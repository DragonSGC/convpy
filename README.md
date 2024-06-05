# Convpy

convpy is a simple command line interface to convert from one base type number to another. It covers
base 2, 8, 10, and 16. convpy will also take in a file containing numbers of one base type and write
the conversions to another file. Orchestrated with the Click Module.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install convpy.

```bash
pip install convpy
```

```bash
pipx install convpy
```

## Usage

To convert one number from the terminal supply the number, its base type, (b - binary, o - octal, d - decimal, x- hexidecimal),
and the base you wish to convert to (-b, -o, -d, -x)

```bash
convpy conv 111 b -d

7
```

convpy supports full paths as well as existance validation on the input file, this command spawns a background process for the
conversion such as not to lock out the terminal incase of large files.

```bash
convpy from-file ./hex_nums.txt ./binary_nums.txt x -b
```

## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)