from .get_all_lines import *

def get_line_numbers_containing_word(file_name, word):
    """
    gets line numbers with string in file
    """
    try:
        lines = get_all_lines(file_name)
    except TypeError:
        lines = file_name
    line_numbers = []
    for i in range(len(lines)):
        if word in lines[i]:
            line_numbers.append(i)
    return line_numbers