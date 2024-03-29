"""
Module handling the connection to the API.
"""

__all__ = [
    "APIConnection"
]

# Imports
import typing
from typing import List, Dict
from rich import print

import aiohttp
from aiohttp import MultipartWriter

from devcord.errors.apierr import InvalidHTTPMethod


class APIConnection:
    """
    Handles a WebSockets connection to the Discord API. Defaults to version 10.

    Parameters:
    - bot_token: The bot token of the bot.
    - version?: The version to choose while connecting to the API.
    """

    def __init__(
        self,
        bot_token: str,
        boundary: str = "boundary",
        version: int = 10
    ):

        self.bot_token = bot_token
        self.boundary = boundary
        self.apiclient: aiohttp.ClientSession = None
        self.baseurl = f"https://discord.com/api/v{version}"

    async def authorize_and_login(self):
        """
        Authorizes the bot token and creates a new connection to the API,
        ready to send and request requests.
        """
        if self.apiclient:
            await self.apiclient.close()

        self.apiclient = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "User-Agent": "DiscordBot (https://github.com/Code-Done-Right/devcord.py, 0.2.0)"
            }
        )
        print("[sea_green2]:D[/sea_green2] [green1]Connected to the API.[/green1]")

    # The multipart maker was creating a ton of bugs and was impeding
    # development for other part of devcord.py. Hence, for now, only
    # text messages can be sent and no files or embedded messages
    # can be sent without an error.

    async def request(
        self,
        method: str,
        endpoint_url: str,
        *,
        payload: Dict = {},
        files: List[str] = []
    ) -> aiohttp.ClientResponse:
        """
        Requests information by using standard HTTP methods.

        Parameters:
        - method: A string denoting the HTTP method.
        - endpoint_url: The endpoint the request should be sent to

        Keyword Parameters:
        - payload?: The JSON payload.
        - files: A list of many file objects with the filename, file content, etc.
        """

        # For now, multipart is not working so directly sending JSON
        async with self.apiclient.request(method, f"{self.baseurl}{endpoint_url}", json=payload) as response:
            if not response.ok:
                print(response.status, response.reason)

            return response
