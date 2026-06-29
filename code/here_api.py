import json
import os
import time

import fw_here as fh
import logger as lg
import requests

# Set the output parameters
TYPE = "Here"
# Coordinates
LAT = 41.1668695
LONG = -8.618076
R = 10000


def fetch_here_data(output_path, here_key, amount_file):
    """
    Function to get the here traffic data
    """
    print("Getting the HERE data...")
    try:
        URL = f"https://data.traffic.hereapi.com/v7/flow?in=circle:{LAT},{LONG};r={R}&locationReferencing=olr&apiKey={here_key}"

        # Get response
        response = requests.get(URL)

        timestamp = int(time.time())
        filename = os.path.join(output_path, TYPE, f"{TYPE}_{timestamp}.json")

        print(response)
        if response.status_code == 200:
            json_data = response.json()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

        # Update the API calls remaining
        fh.set_amount(amount_file=amount_file)

        print(f"Successfully saved active payload to: {filename}")
        lg.log(type=TYPE, logtext=f"{time.time()} - SUCESS: {filename}")

    except Exception as e:
        print(
            f"Intercepted API call but server returned status: {response.status_code}, Error message: {e}"
        )
        lg.log(
            type=TYPE,
            logtext=f"{time.time()} - ERROR: Error getting the reponse code: {response.status_code}. Error message: {e}",
        )
