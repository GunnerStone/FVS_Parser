# gets the indexed word from the line
def get_ith_word_from_line(line, index):
    """
    gets a word from line
    """
    words = line.split()
    return words[index]