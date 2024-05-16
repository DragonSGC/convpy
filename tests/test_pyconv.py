from random import randint

import pytest
from pyconv.pyconv import convert_num


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
    """creates a dictionary with base type flags, 'b', 'o', 'd', 'X' and lists
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
    """Uses the decimal value from base_nums and calls the conversion function
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
    """Makes assertions on established converted permutations to the method
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
    

def test_convert_raises_valueerror(base_nums) -> None:
    """tests whether the converting function will throw out a non valid convert
    flag.

    Args:
        base_nums:pytest fixture returning a Tuple containing 1 each of a bin,
        octal, decimal, and hex number converted from the same decimal number.
    """

    with pytest.raises(ValueError):
        convert_num(int(base_nums[2]), 'k')


def test_for_no_exception_for_correct_conversion_match(base_nums) -> None:
    """tests that the method convert_num does not raise a value error for 
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
