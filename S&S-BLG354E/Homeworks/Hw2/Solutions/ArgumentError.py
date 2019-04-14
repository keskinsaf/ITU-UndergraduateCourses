class  ArgumentError(Exception):
    error_codes_to_messages = {
        0: "Input file is not provided!",
        1: "Format of input file should be mp3!",
    }
    def __init__(self, code):
        self.code = code
    
    def __str__(self):
        return self.error_codes_to_messages[self.code]