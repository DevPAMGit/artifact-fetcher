class ScriptException(Exception):
    """
    Custom exception class for the script.
    """
    def __init__(self, message):
        """
        Initialize a new instance of ScriptException class. ;
        :param message: The exception message. ;
        """
        super(ScriptException, self).__init__()
        self.MESSAGE = message
        