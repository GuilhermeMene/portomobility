import os


def log(type: str, logtext: str):
    """
    Method for save the log in text file
    """

    # Sanitize the string
    logtext = logtext.encode().decode("utf-8")

    try:
        filedir = os.environ.get("PATH_DIR")
        filepath = os.path.join(filedir, f"Log_{type}")

        with open(filepath, "a") as logfile:
            logfile.write(logtext + "\n")
            logfile.close()

    except Exception as e:
        print(f"An error occurred.The log path is inaccessible. Message: {e}")
