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

import os
from random import randint

import pytest
import click
from pyconv.pyconv_calc import (
    convert_num,
    input_to_int,
    input_validation,
    convert_from_file_to_file,
)


@pytest.fixture(scope="module")
def base_nums() -> list:
    """
        Fixture: Creates a random interger in range 1-50 returns a Tuple of
        a single number of each popular base.

    Returns:
        Tuple: Tuple Containing string representations of base 2/8/10/16 numbers
        only one number of each.
    """
    dec_num: int = randint(1, 50)
    bin_num: str = format(dec_num, "b")
    oct_num: str = format(dec_num, "o")
    hex_num: str = format(dec_num, "X")

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
        "b": base_nums[1:],
        "o": [base_nums[0]] + base_nums[2:],
        "d": base_nums[:2] + base_nums[3:],
        "X": base_nums[:3],
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

    base_flags: list = ["b", "o", "d", "X"]

    converted_nums: dict = {
        base: [
            convert_num(int(base_nums[2]), rem_base)
            for rem_base in base_flags
            if rem_base != base
        ]
        for base in base_flags
    }

    return converted_nums


def read_in_file_to_list(input_file: str) -> list:
    """
    Helper function reads a file line by line, appends to a list, returns the
    list
    Args:
        file (str): string file path

    Returns:
        list: list of strings each element a line of the file.
    """
    line_list: list = []

    with open(input_file, "r") as f:
        for line in f:
            line_list.append(line)

    return line_list


@pytest.fixture(scope="module")
def converted_test_data() -> dict:
    """
    Reads in the test file data of binary, octal and hexidecimal numbers from
    the test files, makes them into a list to be used for comparisons in later
    tests.
    Returns:
        dict: dictionary with keys: 'b', 'o', 'x', values are lists from data
        read in from test data.
    """
    test_dir = os.path.dirname(__file__)
    bin_file = os.path.join(test_dir, "bin_nums.txt")
    oct_file = os.path.join(test_dir, "octal_nums.txt")
    hex_file = os.path.join(test_dir, "hex_nums.txt")

    return {
        "b": read_in_file_to_list(bin_file),
        "o": read_in_file_to_list(oct_file),
        "x": read_in_file_to_list(hex_file),
    }


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

    assert all(
        converted_val in conversion_perms["b"] for converted_val in number_perms["b"]
    )
    assert all(
        converted_val in conversion_perms["o"] for converted_val in number_perms["o"]
    )
    assert all(
        converted_val in conversion_perms["d"] for converted_val in number_perms["d"]
    )
    assert all(
        converted_val in conversion_perms["X"] for converted_val in number_perms["X"]
    )


def test_convert_raises_value_error(base_nums) -> None:
    """
    Tests whether the converting function will throw out a non valid convert
    flag.

    Args:
        base_nums:pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    with pytest.raises(ValueError):
        convert_num(int(base_nums[2]), "k")


def test_for_no_exception_for_correct_conversion_match(base_nums) -> None:
    """
    Tests that the method convert_num does not raise a value error for
    expected convert flags.

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    with pytest.raises(ValueError, match=r""):
        convert = convert_num(base_nums[2], "b")
        convert = convert_num(base_nums[2], "o")
        convert = convert_num(base_nums[2], "d")
        convert = convert_num(base_nums[2], "X")

        del convert


def test_binary_validation() -> None:
    """
    Tests validation function if an invalid binary (contains characters other
    than 1's and 0's) is rejected and a valid binary is accepted
    """
    invalid_binary: str = "10001113"
    vaild_binary: str = "10111011"

    assert input_validation(invalid_binary).get("b") is False
    assert input_validation(vaild_binary).get("b") is True


def test_oct_validation() -> None:
    """
    Tests both valid and invalid octal (contains an 8) to see if they are
    accepted or rejected respectively.
    """
    invalid_oct_8: str = "1568"
    invalid_oct_char: str = "133D"
    valid_oct: str = "324"

    assert input_validation(invalid_oct_8).get("o") is False
    assert input_validation(invalid_oct_char).get("o") is False
    assert input_validation(valid_oct).get("o") is True


def test_dec_validation() -> None:
    """
    Tests both valid and invalid decimnal(contains alphabetic values) to see
    if they are accepted or rejected respectively.
    """
    invalid_dec: str = "123456f"
    valid_dec: str = "1234567"

    assert input_validation(invalid_dec).get("d") is False
    assert input_validation(valid_dec).get("d") is True


def test_hex_validation() -> None:
    """
    Test both valid and invalid hexidecimal values(contains characters other
    than A-F or improper form 2a instead of 2A) to see if they are accepted
    or rejected respectively.
    """
    invalid_hex: str = "4H"
    invalid_form_hex: str = "2a"
    valid_hex: str = "4B"

    assert input_validation(invalid_hex).get("x") is False
    assert input_validation(invalid_form_hex).get("x") is False
    assert input_validation(valid_hex).get("x") is True


def test_if_input_to_int_is_accurate(base_nums) -> None:
    """
    Given an input string representing a binary, octal, decimal or hexidecimal,
    is its integer representation accurate

    Args:
        base_nums: pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    assert input_to_int(base_nums[0], "b") == int(base_nums[0], base=2)
    assert input_to_int(base_nums[1], "o") == int(base_nums[1], base=8)
    assert input_to_int(base_nums[2], "d") == int(base_nums[2])
    assert input_to_int(base_nums[3], "x") == int(base_nums[3], base=16)


def test_if_input_to_int_raises_value_error() -> None:
    """
    Given invalid binary, octal, decimal, hexidecimal and base type flag
    """
    with pytest.raises(ValueError):
        input_int = input_to_int("1002", "b")
        input_int = input_to_int("58", "o")
        input_int = input_to_int("23R", "d")
        input_int = input_to_int("5T", "x")
        input_int = input_to_int("12", "h")

        del input_int


def test_if_output_has_been_converted_correctly(converted_test_data) -> None:
    """
    Uses method under test to read in decimal values from a text file and writes
    it to file, output file is read in and made into a list then compared
    against expected values
    Args:
        converted_test_data: pytest fixture with a dictionary of lists
        containing expected data.
    """
    test_dir = test_dir = os.path.dirname(__file__)
    decimal_path = os.path.join(test_dir, "decimal_nums.txt")
    convert_path = os.path.join(test_dir, "convert_output.txt")
    input_path: click.Path = click.Path(
        exists=True, dir_okay=False, file_okay=True
    ).convert(decimal_path, None, None)
    output_path: click.Path = click.Path(exists=False).convert(convert_path, None, None)

    convert_from_file_to_file(input_path, output_path, "d", "b")

    output_list_b: list = read_in_file_to_list(convert_path)

    convert_from_file_to_file(input_path, output_path, "d", "o")

    output_list_o: list = read_in_file_to_list(convert_path)

    convert_from_file_to_file(input_path, output_path, "d", "X")

    output_list_x: list = read_in_file_to_list(convert_path)

    print(output_list_b)

    assert all(
        converted_val in converted_test_data["b"] for converted_val in output_list_b
    )
    assert all(
        converted_val in converted_test_data["o"] for converted_val in output_list_o
    )
    assert all(
        converted_val in converted_test_data["x"] for converted_val in output_list_x
    )


# TODO run click integration tests
