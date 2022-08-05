from utils import *
class ISVALIDOUTPUT:
    def __init__(self,text):
        try:
            self.text = self.get_text(text)
            self.value = self.get_valid_output(self.text)

            # free up memory
            del self.text

        except IndexError as e:
            self.text = None
            self.value = False #default False if not found

    """ gets the text from a FVS_SCAN object's text """
    def get_text(self, text):
        #find the line number that contains the word *ISVALIDOUTPUT
        line_num = get_line_numbers_containing_word(text, '*ISVALIDOUTPUT')[0]

        #get the text from the line
        valid_output_text = get_lines(text, [line_num])[0].split()
        
        return valid_output_text

    """ gets the validoutput flag from the text """
    def get_valid_output(self, text):
        # parse out the isvalidoutput bool value
        # it is the second word in the line
        valid_output_txt = text[1]
        # convert the text to a bool
        valid_output_bool = valid_output_txt.lower() == 'true'
        return valid_output_bool