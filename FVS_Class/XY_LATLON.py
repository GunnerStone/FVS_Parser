from utils import *
class XY_LATLON:
    def __init__(self,text):
        try:
            self.text = self.get_xylatlon_text(text)
            self.x = self.get_x(self.text)
            self.y = self.get_y(self.text)

            # free up memory
            del self.text

        except IndexError as e:
            # print("XY_COORDS not found in text")
            self.text = None
            self.x = None
            self.y = None

    """ gets the statistics text from a FVS_SCAN object's text """
    def get_xylatlon_text(self, text):
        #find the line number that contains the word *XY_LATLON
        line_num = get_line_numbers_containing_word(text, '*XY_LATLON')[0]

        #get the text between the two line numbers
        xylatlon_text = get_lines(text, [line_num])[0].split()
        
        return xylatlon_text

    """ gets the x coordinate from the text """
    def get_x(self, text):
        # parse out the x coordinate and remove the trailing comma
        # it is the second word in the line
        x = text[1].rstrip(',')
        return x

    """ gets the y coordinate from the text """
    def get_y(self, text):
        # parse out the y coordinate and remove the trailing comma
        # it is the third word in the line
        y = text[2]
        return y