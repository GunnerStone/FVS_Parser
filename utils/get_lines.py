from .get_all_lines import get_all_lines

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