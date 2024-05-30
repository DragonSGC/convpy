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

import subprocess
import os
import sys
import click

from pyconv.pyconv_calc import convert_num, input_to_int


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
        convert_to (str): Base to convert the number to ('-b', '-o', '-d', '-x').
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
@click.argument(
    "input_file", type=click.Path(exists=True, dir_okay=False, file_okay=True)
)
@click.argument("output_file", type=click.Path(exists=False))
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
def from_file(
    input_file: click.Path, output_file: click.Path, input_base: str, convert_to: str
) -> None:
    """
    Takes in command line arguments for a file containing numbers of one base
    type, file must exist. An output file to which the converted numbers will
    be written to, file will be created if it doesnt't exist.
    Args:
        input_file (click.Path): File path to file containing numbers of one base
                                type to be converted
        output_file (click.Path): File path to the file which will contain the
                                converted numbers
        input_base (str): Base of the input number ('b', 'o', 'd', 'x').
        convert_to (str): Base to convert the number to ('-b', '-o', '-d', '-x').
    """
    if not convert_to:
        raise click.UsageError(
            "You must specify a target conversion base using -b, -o, -d, or -x."
        )

    # Get the path to the pyconv_calc.py
    script_path = os.path.join(os.path.dirname(__file__), "pyconv_calc.py")
    command = [
        sys.executable,
        script_path,
        input_file,
        output_file,
        input_base,
        convert_to,
    ]

    # Start the process in the background
    subprocess.Popen(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False
    )

    click.echo(
        click.style(
            f"Processing {input_file} in the background. "
            f"Output will be saved to {output_file}.",
            fg="green",
        )
    )
    click.echo(
        click.style(
            "If there were any errors in conversion please see ./pyconc_errors.log",
            fg="red",
        )
    )


if __name__ == "__main__":
    pyconv()
