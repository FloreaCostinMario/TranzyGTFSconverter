import requests
import json
import csv
import zipfile
import os
from tqdm import tqdm
from io import StringIO
from datetime import timedelta
from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv()

API_KEY = os.getenv('TranzyGithubBuildKey') # Replace with your own API key
BASE_URL = "https://api.tranzy.ai/v1/opendata"

######################################################################################################################################
##                                           GTFS files are generated succesfully however                                           ##
##                                             they are invalid because of the absence                                              ##
##                                              of calendar.txt and calendar_dates.txt                                              ##
##                                                   and coresponding parameters                                                    ##
##                                                                                                                                  ##
##        I recommend using these files only if your use case doesn't require perfectly valid GTFS files or schedules               ##
######################################################################################################################################

# Create new session
session = requests.Session()
session.headers.update({
    'X-API-KEY': API_KEY,
    'Accept': 'application/json',
    'User-Agent': 'GTFS Converter/1.0'
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
    #Convert dict to list
    if isinstance(data, dict):
        data = [data]

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

# Functions to fix various parts of the GTFS feed

# Fix route parameters
def FixRoute(RouteTxt):
    FixedRoutes = []

    for Route in RouteTxt:
        #Fix color
        if "route_color" in Route:
            # Tranzy has wierd convetion for white
            if (Route["route_color"] == "#000") or (Route["route_color"] == "000"):
                Route["route_color"] = "000000"
            # Else just remove the # from the string
            else:
                Route["route_color"] = Route["route_color"].replace("#", "")
        
        # Long name should not contain short name for a single route
        if ("route_long_name" in Route) and ("route_short_name" in Route):
            if Route["route_long_name"] == Route["route_short_name"]:
                Route["route_short_name"] = None

        FixedRoutes.append(Route)

    return FixedRoutes

def FixAgency(Agency):
    # For some agencies tranzy provided multiple URLs, this is not supported so only the 1st will be select
    if "agency_urls" in Agency:
        print(type(Agency["agency_urls"]))
        if isinstance(Agency["agency_urls"], list):
            #This agency has issues, copy with all parameters that are lists removed
            FixedAgency = {k: v for k, v in Agency.items() if not isinstance(v, list)}
            FixedAgency["agency_url"] = Agency["agency_urls"][0]
            return FixedAgency

    return Agency

def main():
    print("Starting GTFS generation")

    # Generating agencies and using the Id property for further requests
    Agencies = FetchFromURL(f"{BASE_URL}/agency")

    # Executing agency specific requestss
    for Agency in Agencies:
        # Temporary bypass, Oradea can't be used but is in API
        if Agency["agency_id"] == 9:
            continue

        # Fix agency URLs
        Agency = FixAgency(Agency)

        # Value to contain all csv formated strings
        FilesToGenerate = {}

        Routes = JsonToCSVString(FixRoute(FetchFromURL(f"{BASE_URL}/routes", {"X-Agency-Id" : str(Agency["agency_id"])})))
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
        StopTimes = JsonToCSVString(FetchFromURL(f"{BASE_URL}/stop_times", {"X-Agency-Id" : str(Agency["agency_id"])}))

        # Gather files for compression
        FilesToGenerate.update({
            "agency.txt": JsonToCSVString(Agency),
            "routes.txt": Routes,
            "trips.txt": Trips,
            "stops.txt": Stops,
            "shapes.txt": Shapes,
            "stop_times.txt": StopTimes
        })

        # TO DO: Implemenet version checking

        # Generate feed info
        # Check for version
        
        '''
        Version = 1

        if os.path.exists(f'Output/{Agency["agency_name"]}'):
            with zipfile.ZipFile(f'Output/{Agency["agency_name"]}', 'r') as archive:
                for file_info in archive.infolist():
                    if file_info.filename in FilesToGenerate:
                        with archive.open(file_info.filename) as file:
                            if(file.decode('utf-8') != FilesToGenerate[file_info.filename]):
                                Version += 1 # Bump version
                                archive.close()
                                break
        '''
                                
        FilesToGenerate.update({
            "feed_info.txt", JsonToCSVString(json.loads(json.dumps(
                {
                    "feed_publisher_name": "Florea Costin Mario",
                    "feed_publisher_url": "https://github.com/FloreaCostinMario/TranzyGTFSconverter",
                    "feed_lang": "ron",
                    "feed_contact_url": "https://github.com/FloreaCostinMario/TranzyGTFSconverter/issues",
                    #"feed_version": str(Version)
                }
            )))
        })                   
        
        # Generate gtfs zip archive
        GenerateZIP(f'{Agency["agency_name"]}', FilesToGenerate)

if __name__ == "__main__":
    main()