import json
import os
import time

import logger as lg
import requests

# Set the output parameters
TYPE = "STCP"
URL = "https://broker.fiware.urbanplatform.portodigital.pt/v2/entities?q=vehicleType==bus&limit=1000"


def fetch_stcp_data(output_path):
    """
    Function to get the stcp data from API URL
    """
    try:
        response = requests.get(URL)

        timestamp = int(time.time())
        filename = os.path.join(output_path, TYPE, f"{TYPE}_{timestamp}.json")

        if response.status_code == 200:
            json_data = response.json()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

        print(f"Successfully saved active payload to: {filename}")
        lg.log(type=TYPE, logtext=f"{time.time()} - SUCESS: {filename}")

    except Exception as e:
        print(
            f"Intercepted API call but server returned status: {response.status_code}. Error message: {e}"
        )
        lg.log(
            type=TYPE,
            logtext=f"{time.time()} - ERROR: Error getting the reponse code: {response.status_code}",
        )
