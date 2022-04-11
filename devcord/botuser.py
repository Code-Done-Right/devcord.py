# Imports
import devcord
from devcord.httpconnection import HTTPConnection
from devcord.gatewaywebsocket import GatewayWebSocket

import asyncio


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
        self.bot_token = bot_token
        self.intents = intents
        self.prefixes = prefixes

        self.ws = GatewayWebSocket(self.bot_token, self.intents)
        self.http = HTTPConnection(self.bot_token, 10)

    async def create_session(self, bot_token):
        if not bot_token:
            raise devcord.InvalidSessionError("bot_token")

        else:
            await self.http.login()
            await self.ws.start()

    def run(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.create_session(self.bot_token))

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()

            if self.ws and self.ws.socket:
                loop.run_until_complete(self.ws.socket.close())

            if self.http and self.http.client:
                loop.run_until_complete(self.http.client.close())

            raise devcord.InterruptError(error_type=KeyboardInterrupt)

        except Exception:
            task.cancel()

            if self.ws and self.ws.socket:
                loop.run_until_complete(self.ws.socket.close())

            if self.http and self.http.client:
                loop.run_until_complete(self.http.client.close())

            raise devcord.InterruptError(error_type=Exception)
