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
from random import randint

import pytest
from pyconv.pyconv import (
    convert_num, 
    input_to_int,
    input_validation)


@pytest.fixture(scope='module')
def base_nums() -> list:
    """
        Fixture: Creates a random interger in range 1-50 returns a Tuple of 
        a single number of each popular base.

    Returns:
        Tuple: Tuple Containing string representations of base 2/8/10/16 numbers
        only one number of each.
    """
    dec_num: int = randint(1, 50)
    bin_num: str = format(dec_num, 'b')
    oct_num: str = format(dec_num, 'o')
    hex_num: str = format(dec_num, 'X')

    return [bin_num, oct_num, str(dec_num), hex_num]


@pytest.fixture
def number_perms(base_nums) -> dict:
    """
    Creates a dictionary with base type flags, 'b', 'o', 'd', 'X' and lists
    containing the remaining base type numbers excluding the matching base type

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.

    Returns:
        dict: keys are single character flags matching the base type, 'b' for
        binary etc. values are lists containing the other 3 base type numbers
    """

    return {
        'b': base_nums[1:],
        'o': [base_nums[0]] + base_nums[2:],
        'd': base_nums[:2] + base_nums[3:],
        'X': base_nums[:3]
    }


@pytest.fixture
def conversion_perms(base_nums) -> dict:
    """
    Uses the decimal value from base_nums and calls the conversion function
    for each base number type

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.

    Returns:
        dict: keys are single character flags matching the base type, 'b' for
        binary etc. values are lists containing the other 3 base types after 
        calling the convert function.
    """

    base_flags: list = ['b', 'o', 'd', 'X']

    converted_nums: dict = {base: [convert_num(int(base_nums[2]), rem_base) for 
                                rem_base in base_flags if rem_base != base]
                                for base in base_flags}
    
    return converted_nums


def test_if_conversions_are_accurate(number_perms, conversion_perms) -> None:
    """
    Makes assertions on established converted permutations to the method
    being tested to check method logic to ensure the conversions are happening
    as expected

    Args:
        number_perms:keys are single character flags matching the base type, 
        'b' for binary etc. values are lists containing the other 3 base 
        type numbers.
        conversion_perms:keys are single character flags matching the base type,
        'b' for binary etc. values are lists containing the other 3 base 
        types after calling the convert function.
    """

    assert all(converted_val in conversion_perms['b'] for converted_val 
            in number_perms['b'])
    assert all(converted_val in conversion_perms['o'] for converted_val 
            in number_perms['o'])
    assert all(converted_val in conversion_perms['d'] for converted_val 
            in number_perms['d'])
    assert all(converted_val in conversion_perms['X'] for converted_val 
            in number_perms['X'])
    

def test_convert_raises_value_error(base_nums) -> None:
    """
    Tests whether the converting function will throw out a non valid convert
    flag.

    Args:
        base_nums:pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    with pytest.raises(ValueError):
        convert_num(int(base_nums[2]), 'k')


def test_for_no_exception_for_correct_conversion_match(base_nums) -> None:
    """
    Tests that the method convert_num does not raise a value error for 
    expected convert flags.

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    with pytest.raises(ValueError, match=r""):
        convert = convert_num(base_nums[2], 'b')
        convert = convert_num(base_nums[2], 'o')
        convert = convert_num(base_nums[2], 'd')
        convert = convert_num(base_nums[2], 'X')


def test_binary_validation() -> None:
    """
    Tests validation function if an invalid binary (contains characters other 
    than 1's and 0's) is rejected and a valid binary is accepted
    """
    invalid_binary: str = '10001113'
    vaild_binary: str = '10111011'

    assert input_validation(invalid_binary).get('b') is False
    assert input_validation(vaild_binary).get('b') is True

def test_oct_validation() -> None:
    """
    Tests both valid and invalid octal (contains an 8) to see if they are
    accepted or rejected respectively.
    """
    invalid_oct_8: str = '1568'
    invalid_oct_char: str = '133D'
    valid_oct: str = '324'

    assert input_validation(invalid_oct_8).get('o') is False
    assert input_validation(invalid_oct_char).get('o') is False
    assert input_validation(valid_oct).get('o') is True

def test_dec_validation() -> None:
    """
    Tests both valid and invalid decimnal(contains alphabetic values) to see 
    if they are accepted or rejected respectively.
    """
    invalid_dec: str = '123456f'
    valid_dec: str = '1234567'

    assert input_validation(invalid_dec).get('d') is False
    assert input_validation(valid_dec).get('d') is True


def test_hex_validation() -> None:
    """
    Test both valid and invalid hexidecimal values(contains characters other 
    than A-F or improper form 2a instead of 2A) to see if they are accepted 
    or rejected respectively.
    """
    invalid_hex: str = '4H'
    invalid_form_hex: str = '2a'
    valid_hex: str = '4B'

    assert input_validation(invalid_hex).get('x') is False
    assert input_validation(invalid_form_hex).get('x') is False
    assert input_validation(valid_hex).get('x') is True


def test_if_input_to_int_is_accurate(base_nums) -> None:
    """
    Given an input string representing a binary, octal, decimal or hexidecimal,
    is its integer representation accurate

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    assert input_to_int(base_nums[0], 'b') == int(base_nums[0], base=2)
    assert input_to_int(base_nums[1], 'o') == int(base_nums[1], base=8)
    assert input_to_int(base_nums[2], 'd') == int(base_nums[2])
    assert input_to_int(base_nums[3], 'x') == int(base_nums[3], base=16)


def test_if_input_to_int_raises_value_error() -> None:
    """
    Given invalid binary, octal, decimal, hexidecimal and base type flag
    """
    with pytest.raises(ValueError):
        input_int = input_to_int('1002', 'b')
        input_int = input_to_int('58', 'o')
        input_int = input_to_int('23R', 'd')
        input_int = input_to_int('5T', 'x')
        input_int = input_to_int('12', 'h')