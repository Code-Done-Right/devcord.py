"""
Module holding all gateway error classes.
"""

__all__ = [
    "GatewayError"
]


import typing
from typing import Optional


class GatewayError(Exception):
    def __init__(self, error: Optional[int], code: Optional[str]) -> typing.NoReturn:
        # Error handling
        super().__init__()
