
# get a list of all .out files in the out_files/ directory
import os
import sys

my_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(my_path, ".."))

my_out_files = os.listdir(os.path.join(my_path, "..", "out_files"))
# add the path to the out_files/ directory to the list of files
my_out_files = ["out_files/"+file for file in my_out_files]