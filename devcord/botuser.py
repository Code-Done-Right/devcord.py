"""
Module handling the main bot user.
"""

import asyncio
import typing
from typing import List
from rich import print

from devcord.internals.gatewaywebsocket import GatewayWebSocket
from devcord.internals.apiconnection import APIConnection
from devcord import Intents
from devcord import InterruptionError, BaseError

__all__ = [
    "BotUser"
]


class BotUser:
    """
    A simple class opening 2 websocket connections to receive and send data
    to the Gateway and API.

    Keyword Parameters:
    - bot_token: a string giving your bot's token
    - intents: an integer giving the enabled intents.
    - version?: A version number that denotes the version of the gateway. Defaults to 10.
    - prefixes?: A list of string prefixes that the Gateway will detect
    and respond appropriately.
    """

    def __init__(
        self,
        *,
        bot_token: str,
        intents: int = Intents.All(),
        version: int = 10,
        prefixes: List[str] = []
    ):
        self.token = bot_token
        self.intents = intents
        self.version = version

        self.prefixes = prefixes
        self.api = APIConnection(self.token)
        self.gateway = GatewayWebSocket(
            self.api, self.token, self.intents, self.version)

    async def __start_websocket_sessions(self) -> typing.NoReturn:
        """
        Creates new websocket sessions.
        """
        if self.token:
            await self.api.authorize_and_login()
            await self.gateway.start_websocket()
        else:
            raise Exception

    def run(self):
        """
        Starts a new session when ran properly.
        """
        print(
            f"[sea_green2]:D[/sea_green2] [green1]Thank you for using devcord! <3[/green1]")
        print(f"[sea_green2]:D[/sea_green2] [green1]Want to ask for help, look at devcord's source code, or just chill?[/green1]")
        print(f"[sea_green2]:D[/sea_green2] [green1]Join our Discord! https://discord.gg/r4pudcvBb7[/green1]")
        print(f"[sea_green2]:D[/sea_green2] [green1]Github: https://github.com/Code-Done-Right/devcord.py[/green1]")
        print("[green1]|---------------------------|[/green1]")

        if self.version != 10:
            print(f"[gold3]You specified a version which is not recommended.[/gold3]")

        elif self.version <= 6 or self.version > 10:
            print(
                f"[red1]:/[/red1] [dark_red]You cannot use these versions.[/dark_red]")

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__start_websocket_sessions())
        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            InterruptionError.error(1)
            raise BaseError
