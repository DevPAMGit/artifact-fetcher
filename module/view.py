class View:
    """
    Class representing the script view.
    """

    def __init__(self, maximum: int):
        """
        Initialize a new instance of 'View' class.
        """
        self.MAX: int = maximum
        self.PREVIOUS_MESSAGE_LENGTH: int = 0

        self.INFO: str = "   [INFO] "
        self.ACTION: str = " [ACTION] "
        self.WARNING: str = "[WARNING] "

        self.SUCCESS: str = "[OK]"
        self.ERROR: str = "[ERROR]"

    def __set__previous_message_length(self, length: int):
        """
        Set the class parameter 'PREVIOUS_MESSAGE_LENGTH'. ;
        :param length: The new value of the parameter 'PREVIOUS_MESSAGE_LENGTH'. ;
        """
        self.PREVIOUS_MESSAGE_LENGTH = length

    def __get_space__(self, character: str):
        """
        Get the space necessary fill with a character. ;
        :param character: The fill character. ;
        :return: A string fill with the character in parameter. ;
        """
        maximum: int = self.MAX - self.PREVIOUS_MESSAGE_LENGTH
        index: int = 0

        result: str = ""

        while index < maximum:
            result += character
            index += 1

        return result

    def __print_message__(self, message: str, character: str):
        """
        Print a simple message on the standard output. ;
        :param message:  The message to print to the standard output. ;
        :param character: The filling character. ;
        """
        self.__set__previous_message_length(len(message))
        message += self.__get_space__(character)
        print(message)

    def __print_awaited__(self, message: str):
        self.__set__previous_message_length(len(message))
        print(message, end="")

    def __print_result__(self, result: str, message: str | None, character: str):
        """
        Print the result of an awaited message. ;
        :param result: The success message. ;
        :param character: The filling character. ;
        """
        self.__set__previous_message_length(self.PREVIOUS_MESSAGE_LENGTH + len(result))
        result_message = self.__get_space__(character) + result
        if message is not None:
            result_message += "\n  " + result + " " + message
        print(result_message)

    def title(self, title):
        """
        Print on the standard output the title. ;
        :param title: The title to print. ;
        """
        message: str = ""

        self.__set__previous_message_length(0)
        message += self.__get_space__("-")

        self.__set__previous_message_length(len(title) + 2 + (self.MAX - (len(title) + 2))/2)

        message += "\n|" + self.__get_space__(" ") + title + self.__get_space__(" ") + "|\n"
        self.__set__previous_message_length(0)
        message += self.__get_space__("-")

        print(message)

    def info(self, info: str, character: str):
        """
        Print on the standard output an information. ;
        :param character: The filling character. ;
        :param info: The information to print on the standard output. ;
        """
        self.__print_message__(self.INFO + info + " ", character)

    def warning(self, warning: str):
        """
        Print on the standard output an information. ;
        :param warning: The warning to print on the standard output. ;
        """
        self.__print_message__(self.WARNING + warning + " ", ".")

    def action(self, action: str):
        """
        Print on the standard output an action. ;
        :param action: The error to print on the standard output. ;
        """
        self.__print_awaited__(self.ACTION + action)

    def success(self):
        self.__print_result__(self.SUCCESS, None, ".")

    def error(self, message):
        self.__print_result__(self.ERROR, message, ".")
