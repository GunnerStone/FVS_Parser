from utils import *
class Calibration_Statistics:
    def __init__(self,text):
        self.text = self.get_statistics_text(text)
        self.tree_codes = self.get_tree_codes()
        self.descriptions = self.get_descriptions()
        self.values = self.get_values()

    """ gets the tree codes used within the statistics text"""
    def get_tree_codes(self):
        #find the line that contains the word CALIBRATION STATISTICS
        anchor_line = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[0]
        
        # check if first word in line is CALBSTAT (if yes, then the line is not the tree codes line)
        if self.text[anchor_line].split()[0] == 'CALBSTAT':
            # go to the second occuring line that contains CALIBRATION STATISTICS
            anchor_line = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[1]

        #get the single line that is 3 below the anchor_line number
        #this line contains the tree codes
        my_line = get_lines(self.text, [anchor_line+3])

        #get the number of occuring tree codes
        num_codes = len(my_line[0].split())
        
        # get all tree codes and return them
        tree_codes = []
        for i in range(num_codes):
            tree_codes.append(my_line[0].split()[i])

        return tree_codes

    """ gets the statistics text from a FVS_SCAN object's text """
    def get_statistics_text(self, text):
        #find the line number that contains the word CALIBRATION STATISTICS
        lower_bound = get_line_numbers_containing_word(text, 'CALIBRATION STATISTICS')[0]

        # check if first word in line is CALBSTAT (if yes, then the line is not the tree codes line)
        if text[lower_bound].split()[0] == 'CALBSTAT':
            # go to the second occuring line that contains CALIBRATION STATISTICS
            lower_bound = get_line_numbers_containing_word(text, 'CALIBRATION STATISTICS')[1]

        #find the line number that contains the word MISTLETOE
        upper_bound = get_line_numbers_containing_word(text, 'MISTLETOE')[0]
        upper_bound += 1 # add 1 to include line with mistletoe

        #get the text between the two line numbers
        statistics_text = get_lines(text, range(lower_bound, upper_bound))
        return statistics_text

    """ gets the values from the statistics text """
    def get_values(self):
        # iteritively get the values and add them to a list of dictionaries with the tree code as the key
        values = []

        # iterate through every line in the statistics text
        for line in self.text:
        
            # check if the current line contains x numbers where x is the number of tree codes
            # get the number of numeric values in the line
            line_values = []
            # iterate through every word in the line
            for word in line.split():
                # check if the word is a number
                if is_number(word):
                    line_values.append(word)
            # if the number of numeric values is the same as the number of tree codes
            # then the line contains the values
            if len(line_values) == len(self.tree_codes):
                # dictionary key is the tree code
                my_Values = {}
                # get each numeric value in the line and associate it with its tree code in a dictionary
                for i, value in enumerate(line_values):
                    my_Values[self.tree_codes[i]] = value
                # add the dictionary to the list of values
                values.append(my_Values)

        return values

    def get_descriptions(self):
        descriptions = []

        ignored_keywords = ['NOTE:','DG']

        #find the line that contains the word CALIBRATION STATISTICS
        lower_bound = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[0]
        lower_bound += 5 # add 4 to get to the line after the tree codes line

        #find the line number that contains the word MISTLETOE
        upper_bound = get_line_numbers_containing_word(self.text, 'MISTLETOE')[0]
        upper_bound += 1 # add 1 to include line with mistletoe

        #get the text between the two line numbers
        description_text = get_lines(self.text, range(lower_bound, upper_bound))
        
        description = []
        # iterate through every line in the description text
        for line in description_text:
            numeric_value_found = False
            # read through every word in the line until the word is a number and add it to the list
            for i, word in enumerate(line.split()):
                # check if the first word is a ignored keyword
                if word in ignored_keywords and i == 0:
                    break
                if not is_number(word):
                    description.append(word)
                else:
                    numeric_value_found = True
                    break
            if numeric_value_found == True:
                # convert the list of strings into a string and add it to the list of descriptions
                description = " ".join(description)
                descriptions.append(description)
                description = []

        return descriptions