# Tranzy GTFS converter

This project converts the responses from the https://tranzy.ai API to GTFS static files.

> [!CAUTION]  
> Feeds are not currently published pending last minute compliance checking.

> [!WARNING]  
> Tranzy API isn't fully GTFS compliant, be prepared to troubleshoot.

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/TranzyCreditLight.png">
    <source media="(prefers-color-scheme: light)" srcset="./assets/TranzyCreditDark.png">
    <img alt="Tranzy.ai" src="./assets/TranzyCreditLight.png" style="max-width:120px; height:auto; vertical-align:middle;  margin-right:10px;">
  </picture>
  These files are granted by Tranzy under their own licence which you can read <a href="https://apps.tranzy.ai/accounts/terms-and-conditions" target="_blank" rel="noopener noreferrer">here</a>, additionally each operator has their own individual licence which you can check in the table below.
</p>

<table align="center" style="text-align: center;">
    <thead>
        <tr>
            <th>Operators</th>
            <th>GTFS Files</th>
            <th>Licences</th>
        </tr>
  </thead>
  <tbody>
        <tr>
            <td>
                <a href="https://sctpiasi.ro/">
                    <picture>
                        <source media="(prefers-color-scheme: dark)" srcset="./assets/CTPIasiLight.png">
                        <source media="(prefers-color-scheme: light)" srcset="./assets/CTPIasiDark.png">
                        <img alt="CTP Iasi" src="./assets/CTPIasiDark.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>CTP Iasi</div>
                </a>
            </td>
            <td>GTFS feed soon™</td>
            <td>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/sctp-iasi">Licence</a>
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://ctpcj.ro/">
                    <picture>
                        <img alt="CTP Cluj" src="./assets/CTPCluj.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>CTP Cluj</div>
                </a>
            </td>
            <td>GTFS feed soon™</td>
            <td>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/ctp-cluj">Licence</a>
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://eltransbt.ro/">
                    <picture>
                        <source media="(prefers-color-scheme: dark)" srcset="./assets/ELTRANSBotosaniLight.png">
                        <source media="(prefers-color-scheme: light)" srcset="./assets/ELTRANSBotosaniDark.png">
                        <img alt="Eltrans Botosani" src="./assets/ELTRANSBotosaniDark.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>Eltrans Botosani</div>
                </a>
            </td>
            <td>GTFS feed soon™</td>
            <td>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/eltrans-botosani">Licence</a>
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://stpt.ro/">
                    <picture>
                        <source media="(prefers-color-scheme: dark)" srcset="./assets/STPTLight.png">
                        <source media="(prefers-color-scheme: light)" srcset="./assets/STPTDark.png">
                        <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="./assets/CTPIasiDark.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>STPT Timișoara</div>
                </a>
            </td>
            <td>GTFS feed soon™</td>
            <td>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/stpt-timisoara">Licence</a>
            </td>
        </tr>
        <tr>
            <td>
                <a href="https://rtec.md/">
                    <picture>
                        <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="./assets/RTECChisinau.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>RTEC Chisinau</div>
                </a>
                <a href="https://www.autourban.md/">
                    <picture>
                        <img alt="Shows a black logo in light color mode and a white one in dark color mode." src="./assets/PUAChisinau.png" style="max-width:120px; height:auto; vertical-align:middle;">
                    </picture>
                    <div>PUA Chisinau</div>
                </a>
            </td>
            <td>GTFS feed soon™</td>
            <td>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/rtec-chisinau">RTEC licence</a>
                <br>
                <a href="https://apps.tranzy.ai/accounts/terms-and-conditions/pua-chisinau">PUA licence</a>
            </td>
        </tr>
  </tbody>
</table>

# Realtime feed
Due to limitations of the Tranzy AI (5000 calls / day) & Github limitations, it wasn't possible to add real-time feeds into the scope of this project.

> [!TIP]
> If you want however to have real-time feeds you can register at https://tranzy.dev/accounts, the only real-time feed that the API currently provides is Vehicle Positions.
