import time

import logger as lg


def get_amount(amount_file):
    """
    Method to extract the amount from amount file
    """
    try:
        with open(amount_file, "r") as file:
            print(amount_file)
            lines = [line.rstrip("\n") for line in file]
            print(lines)

            amount = int(lines[0])

        print("The amount has been read.")
        lg.log(
            type="General",
            logtext=f"SUCESS: The amount has been read. Amount: {amount}",
        )

        return amount

    except Exception as e:
        print(f"Cannot read the amount. \n Error message: {e}")
        lg.log(
            type="General",
            logtext=f"{time.time()} - ERROR: Cannot get amount. Error message: {e}",
        )


def set_amount(amount_file, num=1):
    """
    Method to set the amount into the amount file
    """

    try:
        # Get the amount first
        amount = get_amount(amount_file=amount_file)

        # Substract the number of interaction
        amount = amount - num

        # Save the amount into the amount file
        with open(amount_file, "a") as am:
            am.write(str(amount))

        am.close()

        print("The amount has been updated.")
        lg.log(
            type="General",
            logtext=f"SUCESS: The amount has been updated. Amount: {amount}",
        )

    except Exception as e:
        print("Cannot set the amount.")
        lg.log(
            type="General",
            logtext=f"{time.time()} - ERROR: Cannot set amount. Error message: {e}",
        )
