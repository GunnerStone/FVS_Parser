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
