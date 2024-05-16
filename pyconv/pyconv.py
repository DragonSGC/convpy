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

def convert_num(given_num: int, convert_to: str) -> str:
    """Takes in a base 10 interger, uses a flag, to convert to
        match which conversion is correct.

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

