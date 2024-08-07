"""
This module defines the ErrorResponse class for handling error responses.
"""
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """
    Represents an error response with a detailed message and a code.

    Attributes:
        detail (str): A detailed description of the error.
        code (int): The error code associated with the error.
    """
    detail: str
    code: int
