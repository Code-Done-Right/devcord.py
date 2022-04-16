"""
A module holding all classes related to the Bot User.
"""

# Imports
import asyncio

import devcord
from devcord.httpconnection import HTTPConnection
from devcord.gatewaywebsocket import GatewayWebSocket


class BotUser:
    """
    The class containing the bot user information. When initiated with valid parameters,
    it connects to the API and gateway.

    Parameters:
    - bot_token: The token of your bot user.
    - intents?: The intent number of your bot. Defaults to the standard intents,
    i.e `devcord.Intents.Standard`.
    - prefixes?: the list of prefixes the bot uses in case of it using
    prefix commands and/or slash commands.
    """

    def __init__(self, *, bot_token, intents=devcord.Intents.Standard(), prefixes=None):
        """
        Handles the parameters.
        """
        self.bot_token = bot_token
        self.intents = intents
        self.prefixes = prefixes

        self.websocket = GatewayWebSocket(self.bot_token, self.intents)
        self.http = HTTPConnection(self.bot_token, 10)

    async def create_session(self, bot_token):
        """
        Creates a new HTTP and WebSocket session.
        """
        if bot_token:
            await self.http.login()
            await self.websocket.start()

        else:
            raise devcord.InvalidSessionError("bot_token")

    def run(self):
        """
        When called, runs the bot assuming the proper information is inputted
        into the parameters.
        """
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.create_session(self.bot_token))

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt as sessions_interrupted:
            task.cancel()

            if self.websocket and self.websocket.socket:
                loop.run_until_complete(self.websocket.socket.close())

            if self.http and self.http.client:
                loop.run_until_complete(self.http.client.close())

            raise devcord.InterruptError(error_type=KeyboardInterrupt)

        except Exception as general_error:
            task.cancel()

            if self.websocket and self.websocket.socket:
                loop.run_until_complete(self.websocket.socket.close())

            if self.http and self.http.client:
                loop.run_until_complete(self.http.client.close())

            raise devcord.InterruptError(error_type=Exception)
