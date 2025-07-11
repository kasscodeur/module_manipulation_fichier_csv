from typing import Union


def convertir(val: Union[str, int, float]) -> str | int | float:
    """Function to convert data in their original type

    Args:
        val (str | int | float): value to convert to the appropriate type

    Returns:
        (str | int | float): value converted to its appropriete type

    """

    try:
        if val.isdigit():
            return int(val)
        return float(val)
    except ValueError:
        return val.strip()
