"""
Filename: pyconv_calc.py
Author: Simon Crampton
Created: May 16, 2024
Description: This Module contains the logic aspect of the application, converting
            different base type numbers to a base type the user defines

License:
    This code is provided under the GPL V3 License. See the LICENSE file
    for details.
"""

import logging
import sys
from click import Path


# Configure logging
log_filename: str = "pyconv_errors.log"
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(log_filename, mode="w")],
)

logger = logging.getLogger()


def convert_num(given_num: int, convert_to: str) -> str:
    """
    Takes in a base 10 interger, uses a flag, to convert to
        match which conversion is correct.

    Args:
        given_num (int): decimal base 10 number
        convert_to (str): flag description to convert to: b, o, X

    Returns:
        str: string representation of the converted number

    Raises:
        ValueError if convert_to does not match, 'b', 'o', 'd', 'X'
    """
    match convert_to:
        case "b":
            return format(given_num, "b")
        case "o":
            return format(given_num, "o")
        case "d":
            return str(given_num)
        case "X":
            return format(given_num, "X")
        case _:
            raise ValueError("No such base conversion type")


def input_validation(user_input: str) -> dict:
    """
        Takes in a user input and uses boolean character validation on it
    Args:
        user_input (str): user input number to perform validation on

    Returns:
        dict: dictionary with keys being 'b', 'o', 'd', 'x' and values being
            boolean validations
    """
    return {
        "b": all(char in "01" for char in user_input),
        "o": all(char in "01234567" for char in user_input),
        "d": user_input.isdecimal(),
        "x": all(char in "0123456789ABCDEF" for char in user_input),
    }


def input_to_int(input_num: str, input_base: str) -> int:
    """
    Takes a given input number as well as its flag for its base type, either
    'b' for binary, 'o' for octal, 'd' for decimal, 'x' for hexidecimal.
    Performs input validation on the string.

    Args:
        input_num (str): string representation of a number input by user
        input_base (str): flag representing base type of number.

    Returns:
        int: interger value of the user inputted number.

    Raises:
        ValueError on invalid number input and flag input.
    """

    # Enforcing user choice from click.Choice() ensures these will be the values
    base_conversion_functions = {
        "b": lambda num: int(num, base=2),
        "o": lambda num: int(num, base=8),
        "d": int,
        "x": lambda num: int(num, base=16),
    }

    if not input_validation(input_num).get(input_base):
        raise ValueError(f"Invalid {input_base} number")
    try:
        return base_conversion_functions[input_base](input_num)
    except KeyError:
        raise ValueError("Invalid base type flag, only 'b', 'o', 'd' or 'x'")


def convert_from_file_to_file(
    input_path: Path, output_path: Path, input_base: str, convert_to: str
) -> None:
    """
    Takes in two file paths, an input file and output file, using click file
    path validation on the input file. Reads in line by line,  writes the
    converted values to the output file.

    Args:
        input_path (click.Path): Input file path
        output_path (click.Path): output file path, file will be created if it
        doesn't exist
        input_base (str): flag representing base type of numbers in the file.
        convert_to (str): the flag representing the base type to convert to
    """
    with open(input_path, "r") as inp, open(output_path, "w") as out:
        for line_num, line in enumerate(inp, start=1):
            num: str = line.rstrip()
            try:
                converted_num: str = convert_num(
                    input_to_int(num, input_base), convert_to
                )
            except ValueError as ve:
                logger.error("line: %s : %s", line_num, ve)
                out.write("\n")
            else:
                out.write(converted_num + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: convert_from_file_to_file usage <input_file> <output_file>"
            "<input_base> <convert_to>"
        )
        sys.exit(1)
    # Being called from pyconv.py as a child process
    convert_from_file_to_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
