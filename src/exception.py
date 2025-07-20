import sys                                                  # all runtime environment information will be stored in sys 

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = 'Error Message occured in python script name [{0} line number [{1}] error message [{2}]'.format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message


class CustomException(Exception):  #inheritance
    def __init__(self, error_message, error_detail:sys):    #constructor
        super().__init__(error_message)                     # calling parent class - Exception
        self.error_message=error_message_detail(error_message,error_detail=error_detail)  # encapsulation - bundles the traceback info into an object(eror message)

    def __str__(self):
        return self.error_message       # method overriding... overrides parent class