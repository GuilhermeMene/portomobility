# Python module to get data using the specific API's

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import fw_here as fh
import here_api as hr
import ipma_api as ip
import logger as lg
import stcp_api as st
import waze_api as wz

# Set the env file path
global ENV_FILE
try:
    ENV_FILE = str(sys.argv[1])
except Exception as e:
    print(f"The environment path cannot be defined. \n {e}")
    lg.log(
        type="General",
        logtext=f"{time.time()} - ERROR: The environment path cannot be defined. Error message: {e}",
    )

path = "/home/gmap/Documents/Projects/Datascience/Porto/portomobility/.env"


# Set the environment
def set_env():
    """
    Function to read the environment file and set the variables
    """

    global here_key
    global output_path
    global profile_path
    global amount_file

    try:
        with open(path, "r") as file:
            # Stripping the lines by the new line char
            lines = [line.rstrip("\n") for line in file]

            here_key = lines[0]
            output_path = lines[1]
            profile_path = lines[2]
            amount_file = lines[3]
        file.close()

        # Create the folder if not exists
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(profile_path, exist_ok=True)

        # Create data folder if not exists
        os.makedirs(os.path.join(output_path, "Waze"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "Here"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "STCP"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "IPMA"), exist_ok=True)

        # Set the output path for the waze api
        wz.set_output_path(output_path=output_path)

        # Set the path dir for logs
        os.environ["DATA_LOG_PATH"] = output_path

        print("Sucessful read the environment.")
        lg.log(type="General", logtext="SUCESS: The environment has read.")

    except Exception as e:
        print(f"An error occured, the environment cannot be read. \n {e}")
        lg.log(
            type="General",
            logtext=f"{time.time()} - ERROR: The environment file {ENV_FILE} cannot be read. Error message: {e}",
        )


def fetch_data():
    """
    Function to fetch all data using concurrent multi thread pool
    """

    try:
        # Get the amount of the API calls remaining before use the API
        amount = fh.get_amount(amount_file)

        with ThreadPoolExecutor(max_workers=4) as exec:
            # Set the WAZE API
            exec.submit(wz.fetch_waze_data, profile_path)  # Fetch waze traffic data

            # Set the HERE API
            if amount >= 1:
                exec.submit(
                    hr.fetch_here_data, output_path, here_key, amount_file
                )  # Fetch here maps traffic data

            # Set the STCP API
            exec.submit(st.fetch_stcp_data, output_path)  # Fetch stcp bus location data

            # Set the IPMA data
            exec.submit(ip.fetch_ipma_data, output_path)  # Fetch ipma weather data

        print("The Thread pool has been created.")
        lg.log(
            type="General",
            logtext=f"{time.time()} - SUCESS: The thread has been created",
        )

    except Exception as e:
        print(f"The Thread pool cannot be created. \n {e}")
        lg.log(
            type="General",
            logtext=f"{time.time()} - ERROR: The thread cannot be created. Error message: {e}",
        )


if __name__ == "__main__":
    # Set the environment
    set_env()

    # Fetch data
    fetch_data()
