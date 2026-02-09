import sys

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message

        _, _, exc_tb = error_details.exc_info()
        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

        super().__init__(error_message)

    def __str__(self):
        return (
            f"Error occured in python script name [{self.file_name}] "
            f"line number [{self.line_no}] "
            f"error message [{self.error_message}]"
        )
