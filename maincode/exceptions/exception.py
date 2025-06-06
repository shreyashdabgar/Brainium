# create coustem exception for the project 
import sys


def why_error(error, error_details: sys):
    _, _, exc_tb = error_details.exc_info()  # this ( _,_, ) means exc_info() return 3 values but we dont need first two thats why we use ( _ ) to ignore them
    file_name = exc_tb.tb_frame.f_code.co_filename  # for finding file name which file we get error from
    error_message = f"Error in file: {file_name} at line number: {exc_tb.tb_lineno} and the error is: {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self, error, error_details: sys):  # we are taking error and error_details from def error and put into init class because init is package which is used as package and import everywhere
        super().__init__(error)  # we are taking error from def error and put into init class
        self.error = why_error(error_details=error_details, error=error)

    # return error in string format so we can understand easily and read easily 
    def __str__(self):
        return self.error