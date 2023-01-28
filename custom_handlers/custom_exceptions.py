"""
Custom API exceptions.
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    """
    Custom BadRequest exception.
    """
    status_code = 400
    default_detail = "Invalid request parameters. Please check and try again."


class NoContentException(APIException):
    status_code = status.HTTP_204_NO_CONTENT
    default_detail = "No Content"


class UnProcessableEntity(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Un Processable Entity"


class NotOwner(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Not Owner"
