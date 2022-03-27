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