"""
Filename: pyconv.py
Author: Simon Crampton
Created: May 16, 2024
Description: This module functions along with click setup to quickly convert
            numbers to different base types

License:
    This code is provided under the GPL V3 License. See the LICENSE file
    for details.
"""

import click


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
        raise ValueError(f"Invalid {input_base.upper()} number")
    try:
        return base_conversion_functions[input_base](input_num)
    except KeyError:
        raise ValueError("Invalid base type flag, only 'b', 'o', 'd' or 'x'")


@click.group()
def pyconv():
    pass


@pyconv.command()
@click.argument("input_num")
@click.argument(
    "input_base", type=click.Choice(["b", "o", "d", "x"], case_sensitive=False)
)
@click.option("-b", "--binary", "convert_to", flag_value="b", help="Convert to binary")
@click.option("-o", "--octal", "convert_to", flag_value="o", help="Convert to octal")
@click.option(
    "-d", "--decimal", "convert_to", flag_value="d", help="Convert to decimal"
)
@click.option(
    "-x", "--hex", "convert_to", flag_value="X", help="Convert to hexadecimal"
)
def conv(input_num: str, input_base: str, convert_to: str) -> None:
    """
    Convert a number from one base to another.

    Args:
        input_num (str): Number to convert.
        input_base (str): Base of the input number ('b', 'o', 'd', 'x').
        convert_to (str): Base to convert the number to ('b', 'o', 'd', 'X').
    """
    if not convert_to:
        raise click.UsageError(
            "You must specify a target conversion " "base using -b, -o, -d, or -x."
        )

    try:
        click.echo(convert_num(input_to_int(input_num, input_base), convert_to))
    except ValueError as ve:
        click.echo(ve)
    except KeyError as ke:
        click.echo(ke)


@pyconv.command()
def from_file():
    pass


if __name__ == "__main__":
    pyconv()

# TODO investigate how convert command can be run by calling pyconv args
# TODO make the from file run as a background process as not to lock the terminal
