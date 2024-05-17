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
        match which conversion is correct. Raises ValueError if convert_to does
        not match, 'b', 'o', 'd', 'X'

    Args:
        given_num (int): decimal base 10 number
        convert_to (str): flag description to convert to: b, o, X

    Returns:
        str: string representation of the converted number
    """
    match convert_to:
        case 'b':
            return format(given_num, 'b')
        case 'o':
            return format(given_num, 'o')
        case 'd':
            return str(given_num)
        case 'X':
            return format(given_num, 'X')
        case _:
            raise ValueError("No such base conversion type")
        

def binary_input_validation(unvalidated_input: str) -> bool:
    """
    Checks to see if only '1' and '0' are present in the input

    Args:
        unvalidated_input (str): user inputted number for conversion

    Returns:
        bool: return True or False depending on the outcome of the validation
    """
    return all(char in '01' for char in unvalidated_input)


def oct_input_validation(unvalidated_input: str) -> bool:
    """
    Uses isdecimal() as well as checking there are no 8's in the input

    Args:
        unvalidated_input (str): user inputted number for conversion

    Returns:
        bool: return True or False depending on the outcome of the validation
    """
    if unvalidated_input.isdecimal():
        return all(char not in '8' for char in unvalidated_input)
    else:
        return False


def dec_input_validation(unvalidated_input: str) -> bool:
    """
    Uses isdecimal() to validate, octal and decimal such that they 
    only contain decimal values.

    Args:
        unvalidated_input (str): user inputted number for conversion

    Returns:
        bool: return True or False depending on the outcome of the validation
    """
    return unvalidated_input.isdecimal()


def hex_input_validation(unvalidated_input: str) -> bool:
    """
    Uses isalnum() in conjuction with a list A-F to represent accepted
    hexidecimal numbers ie 6Z would be invalid.

    Args:
        unvalidated_input (str): user inputted number for conversion

    Returns:
        bool: return True or False depending on the outcome of the validation
    """
    if unvalidated_input.isalnum():
        return all(char in '123456789ABCDEF' for char in unvalidated_input)
    else:
        return False
    

def input_to_int(input_num: str, input_base: str) -> int:
    """Takes a given input number as well as its flag for its base type, either
    'b' for binary, 'o' for octal, 'd' for decimal, 'x' for hexidecimal. 
    Performs input validation on the string with for Raises ValueError on 
    invalid number input and flag input

    Args:
        input_num (str): string representation of a number input by user
        input_base (str): flag representing base type of number

    Returns:
        int: interger value of the user inputted number
    """
    match input_base:
        case 'b':
            if  not binary_input_validation(input_num):
                raise ValueError("Invalid Binary number")
            return int(input_num, base=2)
        case 'o':
            if not oct_input_validation(input_num):
                raise ValueError("Invalid Octal number")
            return int(input_num, base=8)
        case 'd':
            if not dec_input_validation(input_num):
                raise ValueError("Invalid Decimal number")
            return int(input_num)
        case 'x':
            if not hex_input_validation(input_num):
                raise ValueError("Invalid Hexidecimal number")
            return int(input_num, base=16)
        case _:
            raise ValueError("Invalid base type flag, only 'b', 'o', 'd' or 'x"\
                            "type pyconv --help for more information")
        

@click.command
@click.argument('input_num')
@click.argument('input_base')
@click.option('-b', '--binary', flag_value='b', help='dets the target of the ' \
            'conversion to binary')
@click.option('-o', '--octal', flag_value='o', help='dets the target of the ' \
            'conversion to octal')
@click.option('-d', '--decimal', flag_value='d', help='dets the target of the ' \
            'conversion to decimal')
@click.option('-x', '--hex', flag_value='x', help='dets the target of the ' \
            'conversion to hexidecimal')
def pyconv(input_num: str, input_base: str,binary: str, octal: str, 
            decimal: str, hex: str, ) -> None:
    """
        Takes in the input number and input base ('b', 'o', 'd', 'x') and a flag
        to convert the number to a different base type.
    """
    options_list = [binary, octal, decimal, hex]

    if input_base in options_list:
        click.echo(input_num)
        return

    for option in options_list:
        if option is not None:
            try:
                click.echo(convert_num(input_to_int(input_num, input_base), 
                                    option))
            except ValueError as ve:
                click.echo(ve)


if __name__ == '__main__':
    pyconv()    

