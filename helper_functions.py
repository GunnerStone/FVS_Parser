"""
 helper functions to help read file io
"""
# returns all lines from file
def get_all_lines(file_name):
    """
    gets all lines from file
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    return lines

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

# returns all desired lines from file
def get_lines(file_name, line_numbers):
    """
    gets lines from file
    """
    try:
        lines = get_all_lines(file_name)
    except TypeError:
        lines = file_name
    lines_to_return = []
    for line_number in line_numbers:
        lines_to_return.append(lines[line_number])
    return lines_to_return

# checks if a string is a number
def is_number(s):
    """
    checks if string is a number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

# gets the indexed word from the line
def get_ith_word_from_line(line, index):
    """
    gets a word from line
    """
    words = line.split()
    return words[index]


# get the indent level of the line
def get_indent_level(line):
    """
    gets indent level of line
    """
    indent_level = 0
    for char in line:
        if char == ' ':
            indent_level += 1
        else:
            break
    return indent_level

# return all lines that match the desired indent level
def get_lines_with_indent_level(file_name, indent_level):
    """
    gets lines with indent level
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines_to_return = []
    for line in lines:
        if get_indent_level(line) == indent_level:
            lines_to_return.append(line)
    return lines_to_return

def get_index_of_word_within_line(line, word):
    """
    gets index of word within line
    """
    indexes = []
    words = line.split()
    for i in range(len(words)):
        if words[i] == word:
            indexes.append(i)
    return indexes