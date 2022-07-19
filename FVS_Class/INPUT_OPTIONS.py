from calendar import c
from collections import Counter
from utils import *
import time
class INPUT_OPTIONS:
    def __init__(self,text):
        try:
            self.text = self.get_text(text)
            self.dictionary = self.parse_data(self.text)

            # free up memory
            del self.text

        except IndexError as e:
            self.text = None
            self.dictionary = None

    """ gets the statistics text from a FVS_SCAN object's text """
    def get_text(self, text):
        #find the line number that contains the word OPTIONS SELECTED BY INPUT
        first_line_num = get_line_numbers_containing_word(text, 'OPTIONS SELECTED BY INPUT')[0]

        #find the last number (contains the text OPTIONS SELECTED BY DEFAULT)
        last_line_num = get_line_numbers_containing_word(text, 'OPTIONS SELECTED BY DEFAULT')
        
        # only get the line that ONLY contains the word OPTIONS SELECTED BY INPUT
        for line_num in last_line_num:
            if len(get_lines(text, [line_num])[0].split()) == 4:
                last_line_num = line_num - 2

        #get the text between the two line numbers
        text = get_lines(text, range(first_line_num, last_line_num))
        return text

    """ gets the x coordinate from the text """
    def parse_data(self, text):
        my_dict = {}

        # go down the lines until you find the first instance of the word PARAMETERS:
        start_line_num = None
        for i, line in enumerate(text):
            if 'PARAMETERS:' in line:
                start_line_num = i
                break
        # go past the ------- and the blank line
        start_line_num+=3
        
        params = []
        values = []
        comments = "COMMENTS:"

        param_name = None
        param_value = None

        # cheapo_flag = False

        for e, line in enumerate(text[start_line_num:]):
            # print("e: ", e)
            # print(len(text[start_line_num:]))
            # print("line: ",line)
            # if line is blank, skip it
            # print("line: ",line)
            # print("line.split(): ",line.split())
            
            # print("Num of words in line: ", len(line.split()))
                
            # if line does not start with spaces, it is the start of a new parameter
            # if line is not an empty list
            if len(line.split()) > 0:
                # if line.split()[0] == "CHEAPO":
                #     print("ON THE CHEAPO LINE")

                if line[0] != ' ' and len(line.split())>0:
                    # if line.split()[0] == "CHEAPO":
                    #     print("CHEAPO IS A PARAMETER")
                    # print("LINE IS PARAMETER: ", line)
                    # get the parameter name
                    param_name = line.split()[0]
                    
                    # get the parameter value
                    param_value = ' '.join(line.split()[1:])
                    # if parameter value is None, make it an empty string
                    if param_value is None:
                        param_value = ''
                    # if line.split()[0] == "CHEAPO":
                    #     print("param_name: ", param_name)
                    #     print("param_value: ", param_value)
                    #     print("e: ", e)
                    #     cheapo_flag = True
                    #     time.sleep(3)

                # if the line starts with spaces, it is a continuation of the previous parameter
                elif line[0] == ' ' and len(line.split())>0:
                    # if line.split()[0] == "CHEAPO":
                    #     print("CHEAPO IS A CONTINUATION")
                    #     time.sleep(3)
                    # print("LINE IS CONTINUATION: ", line)
                    # check if its a comment line by checking if first word starts with a *
                    if line.split()[0][0] == '*':
                        # get the comment
                        comments += '\n' + ' '.join(line.split())
                    # if not a comment line, add the line to the value
                    else:
                        if param_value is not None:
                            param_value += '\n' + ' '.join(line.split())
            elif len(line.split()) == 0:
                # if cheapo_flag:
                #     print("e: ", e)
                #     print("line is blank")
                #     time.sleep(3)
                # print("LINE IS BLANK: ", line)
                # after reading a completed parameter, the next line will be blank
                # and enter this conditional, appending the parameter to the dictionary
                if e < (len(text[start_line_num:]) - 2):
                    # print("found blank line & its not close to last line")
                    # check if the next line is a value
                    if text[start_line_num + e + 1][0] == ' ' and len(text[start_line_num + e + 1].split()) > 0:
                        # if it is, just continue the loop and have the line get picked up and appended
                        # if cheapo_flag:
                        #     print("cheapo is triggering a 1 line buffer")
                        #     time.sleep(3)
                        continue
                    elif text[start_line_num + e + 2][0] == ' ' and len(text[start_line_num + e + 2].split()) > 0 and len(text[start_line_num + e + 1].split()) == 0:
                        # if cheapo_flag:
                        #     print("cheapo is triggering a 2 line buffer")
                        #     time.sleep(3)
                        continue

                # do the above but with a loop until you find a non-blank line
                # while (text[start_line_num+e+1][0] == " "):
                # if cheapo_flag:
                #     print("cheapo is getting appended???")
                #     time.sleep(3)
                params.append(param_name)
                values.append(param_value)
                param_name = None
                param_value = None
                continue
            # special case for the last line
            # if e == 0:
            #     time.sleep(3)
            if e == len(text[start_line_num:]):
                params.append(param_name)
                values.append(param_value)
                param_name = None
                param_value = None

        

        # find all indexes in params where it is none
        none_idxs = [i for i, x in enumerate(params) if x is None]
        # remove all the None values from the params and values lists
        for i in none_idxs[::-1]: # reverse the list so popping works
            params.pop(i)
            values.pop(i)

        # find duplicate parameters and rename them to avoid conflicts
        duplicated_params = []
        for i, param in enumerate(params):
            if param in duplicated_params:
                param = param + "_duplicateKeyToken(" + str(i) + ")"
                duplicated_params.append(param)
            else:
                duplicated_params.append(param)

        params = duplicated_params
        
        # dictionary comprehension to stitch the params and values together
        input_options_dict = {params[i]: values[i] for i in range(len(params))}
        # add the comments to the dictionary
        input_options_dict['COMMENTS'] = comments


       

        # remove all null values and their corresponding keys from the dictionary
        # null values are duplicate keys, we ignore them to avoid errors with mongodb
        input_options_dict = {k: v for k, v in input_options_dict.items() if v is not None}
        
        

        return input_options_dict