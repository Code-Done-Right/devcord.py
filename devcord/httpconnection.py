# Imports
import aiohttp
from aiohttp import ClientSession


class HTTPConnection:
    """
    The client sending requests related to the Discord REST API. Initialised
    automatically at around the same time websocket is launched.

    TODO:
    For the implementation of sending embedded messages such as images, files, or
    embeds themselves, multipart will be implemented soon.

    Parameters:
    - bot_token: The token of the bot
    - version: The API version
    """

    def __init__(self, bot_token: str, version: int):
        # Bot User
        self.bot_token = bot_token
        self.version = version

        # HTTP Client and API
        self.client: aiohttp.ClientSession = None
        self.API_URL = f"https://discord.com/api/v{self.version}"
        self.CDN_URL = f"https://cdn.discordapp.com/"

    async def login(self):
        """
        Creates a completely new session.

        Refer:
        https://discord.com/developers/docs/reference#http-api
        """
        if self.client:
            await self.client.close()

        self.client = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bot {self.bot_token}",
                "User-Agent": "devcord (https://github.com/Code-Done-Right/devcord.py v1.0.0)",
            }
        )

    async def request(self, payload, session, parameters=None, files=None):
        """
        Sends a request to the Discord API when called with the right parameters.

        Parameters:
        - payload: The JSON payload to be requested. Make it a valid payload!
        - session: The client session.
        - parameters?: The params for anything (TODO will be worked on)
        - files?: Optional files to be sent to the API (TODO will also be worked on)
        """
        self.payload = payload
        self.session = session
        self.files = files
