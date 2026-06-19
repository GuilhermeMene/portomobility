import json
import os
import time

import logger as lg
import requests

# Set the output parameters
TYPE = "Here"
OUTPUT_DIR = os.environ.get("PATH_DIR")
print(OUTPUT_DIR)
# OUTPUT_DIR = f"../Data/{TYPE}"
# Coordinates
LAT = 41.1668695
LONG = -8.618076
R = 10000

try:
    # Get the env variables
    key = os.environ.get("HERE_KEY")
    print(key)
    URL = f"https://data.traffic.hereapi.com/v7/flow?in=circle:{LAT},{LONG};r={R}&locationReferencing=olr&apiKey={key}"

    # Get response
    response = requests.get(URL)

    timestamp = int(time.time())
    filename = os.path.join(OUTPUT_DIR, f"{TYPE}_{timestamp}.json")

    if response.status_code == 200:
        json_data = response.json()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

    print(f"Successfully saved active payload to: {filename}")
    lg.log(type="Here", logtext=f"SUCESS: {filename}")

except Exception as e:
    print(f"Intercepted API call but server returned status: {response.status_code}")
    lg.log(
        type=TYPE,
        logtext=f"ERROR: Error getting the reponse code: {response.status_code}",
    )
