"""
Module handling general interruptions and errors.
"""

import typing

from rich import print

__all__ = [
    "InterruptionError"
]


class BaseError(Exception):
    """
    Raised to inform the use to check the prompt.
    """

    def __init__(self) -> None:
        super().__init__("Please check the error log written in red, and the traceback.")


class InterruptionError:
    """
    Raised when an interruption, especially KeyboardInterrupt, occurs.
    """

    @classmethod
    def error(cls, type: int):
        """
        Common method for raising the final error. Read `__init__.py`.
        """
        if type == 1:
            print(
                "[red1]:/[/red1] [bright_red]You created a keyboard interrupt.[/bright_red]")
