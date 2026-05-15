"""
Standardised API response helpers.
Use these to keep response shape consistent across endpoints.
"""

from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """Return a uniform success envelope."""
    return Response(
        {
            "status": "success",
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def error_response(message="An error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Return a uniform error envelope."""
    return Response(
        {
            "status": "error",
            "message": message,
            "errors": errors,
        },
        status=status_code,
    )
