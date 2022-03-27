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