from .get_indent_level import get_indent_level

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