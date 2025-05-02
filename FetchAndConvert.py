import requests
import json
import csv
import configparser
import zipfile
from tqdm import tqdm
from io import StringIO
from datetime import timedelta
from ratelimit import limits, sleep_and_retry
import os

API_KEY = os.getenv('TranzyGithubBuildKey')
BASE_URL = "https://api.tranzy.ai/v1/opendata"

# Create new session
session = requests.Session()
session.headers.update({
    'X-API-KEY': API_KEY,
    'Accept': 'application/json'
})

# Main http request function
# Setup rate limiting
@sleep_and_retry
@limits(calls=4, period=timedelta(seconds=1).total_seconds())
def FetchFromURL(URL: str, headers=None, params=None):
    try:
        response = session.get(URL, headers=headers, params=params)
        response.raise_for_status()
        
        # Automatically parse json
        if 'application/json' in response.headers.get('Content-Type', ''):
            return response.json()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
        
# Converting API responses to CSV/TXT
def JsonToCSVString(data):
    #Storing conversion result in buffer
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    #First entry should have all keys
    csv_writer.writerow(data[0].keys())
    #The data itself
    for row in data:
        csv_writer.writerow(row.values())

    #Get final buffer value
    return csv_buffer.getvalue().encode('utf-8')

# Generating gtfs archive
def GenerateZIP(Name: str, files):
    with zipfile.ZipFile(f'Output/{Name}.zip', 'w') as zipf:
        for filename, content in files.items():
            zipf.writestr(filename, content)

def main():
    print("Starting GTFS generation")

    # Generating agencies and using the Id property for further requests
    Agencies = FetchFromURL(f"{BASE_URL}/agency")
    AgenciesCSV = JsonToCSVString(Agencies)

    # Executing agency specific requestss
    for Agency in Agencies:
        # Value to contain all csv formated strings
        FilesToGenerate = {}

        Routes = JsonToCSVString(FetchFromURL(f"{BASE_URL}/routes", {"X-Agency-Id" : str(Agency["agency_id"])}))
        Trips = FetchFromURL(f"{BASE_URL}/trips", {"X-Agency-Id" : str(Agency["agency_id"])})
        
        # Generate shapes for each trip
        print("Start shape generation")

        Shapes = json.loads('[]')        
        for Trip in tqdm(Trips, desc="Fetching shapes", unit="shape"):        
            TripShape = FetchFromURL(f"{BASE_URL}/shapes", {"X-Agency-Id" : str(Agency["agency_id"])}, {"shape_id": Trip["shape_id"]})
            Shapes += TripShape
        
        # Convert used jsons to csv format
        Trips = JsonToCSVString(Trips)
        Shapes = JsonToCSVString(Shapes)

        Stops = JsonToCSVString(FetchFromURL(f"{BASE_URL}/stops", {"X-Agency-Id" : str(Agency["agency_id"])}))
        StopTimes = JsonToCSVString(FetchFromURL(f"{BASE_URL}/stops", {"X-Agency-Id" : str(Agency["agency_id"])}))

        # Gather files for compression
        FilesToGenerate.update({
            "agency.txt": AgenciesCSV,
            "routes.txt": Routes,
            "trips.txt": Trips,
            "stops.txt": Stops,
            "shapes.txt": Shapes,
            "stop_times.txt": StopTimes
        })
        
        # Generate gtfs zip archive
        GenerateZIP(f'{Agency["agency_id"]}', FilesToGenerate)

if __name__ == "__main__":
    main()