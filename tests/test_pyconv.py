"""
Filename: test_pyconv.py
Author: Simon Crampton
Created: May 16, 2024
Description: Contains the unit tests for the pyconv.py file

License:
    This code is provided under the GPL V3 License. See the LICENSE file
    for details.
"""

import pytest
from click.testing import CliRunner

from pyconv.pyconv import pyconv


@pytest.fixture
def runner() -> CliRunner:
    """
        Fixture that creates an instance of the CliRunner class from click.testing

    Returns:
        CliRunner: _CliRunner object to be used in tests
    """
    return CliRunner()


def test_if_usage_error_is_raised_correctly_for_missing_input(runner) -> None:
    """
    Test invokes the conv command and purposely uses an incorrect
    option to see if the application raises the exception.

    Args:
    runner (CliRunner): A pytest fixture representing a CliRunner object
    """

    result = runner.invoke(pyconv, ["conv", "111", "b"])
    assert result.exit_code == 2
    assert (
        "You must specify a target conversion "
        "base using -b, -o, -d, or -x." in result.output
    )


def test_if_input_is_taken_in_correctly(runner) -> None:
    """
    Test to see if a correct user input is being recorded and invoking the correct
    methods

    Args:
        runner (CliRunner): A pytest fixture representing a CliRunner object
    """

    result = runner.invoke(pyconv, ["conv", "111", "b", "-d"])

    assert result.exit_code == 0
    assert "7" in result.output
