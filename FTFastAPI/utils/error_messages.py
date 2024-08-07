from enum import Enum

class ErrorMessages(Enum):
    """
    Enum class representing common error messages used throughout the application.

    Attributes:
        USER_ALREADY_REGISTERED (str): Message indicating that the user is already registered.
        INCORRECT_CREDENTIALS (str): Message indicating incorrect username or password.
        TOKEN_VERIFICATION_FAILED (str): Message indicating that token verification failed.
    """
    INTERNAL_SERVER_ERROR = "Internal Server Error"
