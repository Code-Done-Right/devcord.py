# Imports
import aiohttp
from aiohttp import ClientSession

from base64 import b64decode

class HTTPConnection:
    """
    The client sending requests related to the Discord REST API. Initialised
    automatically at around the same time websocket is launched.

    For the implementation of sending embedded messages such as images, files, or
    embeds themselves, multipart will be implemented soon.

    Parameters:
    - bot_token: The token of the bot
    - version: The API version
    """

    def __init__(self, bot_token: str, version: int):

        # HTTP Client and API
        self.client_id = b64decode(bot_token[:24])
        self.client: aiohttp.ClientSession = None
        self.API_URL = f"https://discord.com/api/v{version}"

        # Application commands
        self.APPLICATION_COMMAND_TYPES = {
            "CHAT_INPUT": 1,
            "USER": 2,
            "MESSAGE": 3
        }
        self.CHAT_INPUT_REGEX = "^[\w-]{1,32}$"

    def request(self, payload, session, parameters = None, files = None):
        """
        Sends a request to the Discord API when called with the right parameters.

        Parameters:
        - payload: The JSON payload to be requested. Make it a valid payload!
        - session: The Client session.
        - parameters?: The params for anything (TODO will be worked on)
        - files?: Optional files to be sent to the API (TODO will also be worked on)
        """
        self.payload = payload
        self.session = session
        self.files = files