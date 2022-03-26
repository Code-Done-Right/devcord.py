# Imports
import devcord
from devcord.httpconnection import HTTPConnection
from devcord.gatewaywebsocket import GatewayWebSocket

import asyncio


class BotUser:
    """
    The class containing the bot user information. When initiated with valid params,
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

        self.ws = GatewayWebSocket("placeholder", self.bot_token, self.intents)
        self.http = HTTPConnection("placeholder", 9)

    async def create_session(self, bot_token):
        if not bot_token:
            bot_token = ""

        await self.http.login()
        await self.ws.start()

    def run(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.create_session(self.bot_token))

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()

            if self.ws and self.ws.sock:
                loop.run_until_complete(self.ws.sock.close())

            if self.http and self.http.session:
                loop.run_until_complete(self.http.session.close())
