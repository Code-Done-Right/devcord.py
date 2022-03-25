# Imports
import aiohttp
from aiohttp import ClientSession

import json

class HTTPConnection:
    """
    The client sending requests related to the Discord REST API. Initialised
    automatically at around the same time websocket is launched.
    This connection also handles the sending of files and images, through the
    CDN. All files and requests are to be received from the bot user.

    TODO:
    For the implementation of sending embedded messages such as images, files, or
    embeds themselves, multipart will be implemented soon.

    Parameters:
    - bot_token: The token of the bot
    - version: The API version
    """

    def __init__(self, bot_token: str, version: int, boundary="boundary"):
        # Bot User
        self.bot_token = bot_token
        self.version = version

        # HTTP Client and API
        self.client: aiohttp.ClientSession = None
        self.API_URL = f"https://discord.com/api/v{self.version}"
        self.CDN_URL = f"https://cdn.discordapp.com/"

        self.boundary = boundary

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

    async def create_multipart(self, data, files) -> bytes:
        """Create the multipart used when sending attachments through Discord
        
        Arguments:
            data (Any): Any valid JSON object, provided as `payload_json`
            files (List[pycordia.models.File]): The files to be sent in the message
        Returns:
            A bytes object containing the constructed multipart string
        """
        multipart = (f'--{self.boundary}\n' \
                      'Content-Disposition: form-data; name="payload_json"\n' \
                      'Content-Type: application/json\n\n' \
                     f'{json.dumps(data, indent=4)}\n').encode("utf-8")

        for i, fl in enumerate(files):
            multipart += (f'--{self.boundary}\n' \
                          f'Content-Disposition: form-data; name="files[{i}]"; filename="{fl.filename}"\n' \
                           'Content-Type: application/octet-stream\n\n').encode("utf-8") + fl.fp.read() + b"\n"
        multipart += f"--{self.boundary}--".encode("utf-8")

        return multipart

    async def request(self, method, endpoint, *, payload, parameters=None, files=None):
        """
        Sends a request to the Discord API when called with the right parameters.

        Parameters:
        - method: The name of any valid HTTP keyword (GET, POST, PATCH, etc.)
        - endpoint: A valid endpoint. Eg: https://cdn.discordapp.com/emojis/....png

        Keyword Parameters:
        - payload: The JSON payload to be requested. Make it a valid payload!
        - session: The client session.
        - parameters?: The query params for any URL
        - files?: Optional files to be sent to the API
        """
        if not payload:
            payload = {}
        if not parameters:
            parameters = {}

        if not self.client:
            raise Exception # TODO

        param_list = []
        if parameters:
            for name, value in parameters.items():
                if value is None:
                    continue

                param_list.append(f"{name}={value}")

            if param_list:
                endpoint = f"{endpoint}?{'&'.join(param_list)}"

        if files:
            multipart = await self.create_multipart(payload, files)
            content_type = f'multipart/form-data; boundary="{self.boundary}"'

            kws = { "data": multipart }
        else:
            multipart = ""
            content_type = "application/json"
            kws = { "json": payload } if payload else {}

        async with self.client.request(
            method, f"{self.API_URL}/{endpoint}", 
            **kws, headers={ "Content-Type": content_type }
        ) as resp:
            if resp.status == 204:
                async def json(**kwargs):
                    return {}
                resp.json = json
                
                return resp

            rs = await resp.json()

            if not resp.ok:
                raise Exception # TODO
            
            return resp