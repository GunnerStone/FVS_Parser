from utils import *
class VERSION_NUM:
    def __init__(self,text):
        try:
            self.text = self.get_version_text(text)
            self.version = self.get_version(self.text)

            # free up memory
            del self.text

        except IndexError as e:
            # print("XY_COORDS not found in text")
            self.text = None
            self.version = None

    """ gets the statistics text from a FVS_SCAN object's text """
    def get_version_text(self, text):
        #find the line number that contains the word *XY_COORDS
        line_num = get_line_numbers_containing_word(text, 'FOREST VEGETATION SIMULATOR     VERSION')[0]

        #get the text on the line number
        xycoords_text = get_lines(text, [line_num])[0].split()
        
        return xycoords_text

    """ gets the x coordinate from the text """
    def get_version(self, text):
        # parse out the x coordinate and remove the trailing comma
        # it is the fifth word in the line
        version = text[4]
        return version