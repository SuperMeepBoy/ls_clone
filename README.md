# Ls clone in Python

This project is a clone of the `ls` command in Python.
To know about ls, check the [ls man page](http://www.man7.org/linux/man-pages/man1/ls.1.html).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run the program you need Python3 installed on your machine.

You also need to install the libraries required which are contained in the requirements.txt file.

If you have pip installed, you can do so by running the command `pip install -r requirements.txt`.

### Running the command

To run the program, run the main.py file located in the src folder.

```
Usage:
  main.py [-a] [-R] [-l] [-c] [-d] [-r] [-S] [<file>]
  main.py -h | --help
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

  -a            Include hidden files.
  -R            Recursive search.
  -l            Display files size.
  -c            Display files number of lines.
  -d            Only display folders and number of files within them.
  -r            Reverse display order.
  -S            Sort by size.
```

## Running the tests

Tests are run using pytest so you need pytest installed. All testing requirements can be installed using pip with the following command `pip install -r testing-requirements.txt`.

To run the tests, run the command : `PYTHONPATH=./src py.test tests -v` (`-v` adds verbosity)
If you want to see the coverage, run : `PYTHONPATH=./src py.test --cov=tests/ -v`

## Authors

* **Jef Roelandt** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
