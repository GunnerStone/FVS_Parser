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