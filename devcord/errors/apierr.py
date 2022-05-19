"""
"""

import typing
from rich import print

__all__ = [
    "InvalidRequest",
    "InvalidHTTPMethod"
]


class InvalidRequest:
    """
    Base class for all problems in requesting to the API.
    """

    def __init__(self) -> typing.NoReturn:
        pass

    def error(self, error_type):

        # Invalid method
        if error_type == 0:
            message = "[red1]:/[/red1] [bright_red]The request method is invalid or incorrect. Please report this to the devs![/bright_red]"

        # Invalid URL
        if error_type == 1:
            message = "[red1]:/[/red1] [bright_red]The enpoint is invalid or incorrect. Please report this to the devs![/bright_red]"

        else:
            message = "placeholder"

        print(message)


class InvalidHTTPMethod:
    """
    Exception class for invalid HTTP methods.
    """

    @classmethod
    def error(cls) -> typing.NoReturn:
        print("[red1]:/[/red1] [bright_red]Your HTTP method is invalid.[/bright_red]")
        raise Exception
