import sys
import re


# return a file content as string
# Raise OSError if file not found
def read_file(file_name):
    with open(file_name, "r") as file:
        input_text = file.read()
    return input_text


# return first command line argument
# Raise IndexError if no arguments
def get_first_command_line_argument():
    if len(sys.argv) < 2:
        raise IndexError("Expected an input file argument")
    return sys.argv[1]


# return string after re.match usage
def apply_regex(regex, input):
    return re.match(regex, input)


# return the lowest index in input where substring is found
# if substring not found, return int max value
def get_next_substring_index(input, substring):
    index = input.find(substring)
    if index < 0:
        index = sys.maxsize
    return index


# print output text to stdout
def print_stdout(output_text):
    print(output_text)
