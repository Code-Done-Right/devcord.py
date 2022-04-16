"""
A module containing everything that is related to the web socket connection
to the Discord Gateway. The default is v10.
"""


# Imports
import zlib
import json
from colorama import Fore

import aiohttp
from aiohttp import WSMsgType
import asyncio
from devcord import Intents, GatewayErrors


class GatewayWebSocket:
    """
    A class creating the Gateway websocket. Handles all gateway events such as
    opcodes, heartbeats and ACKs, etc.

    Starts with sending `IDENTIFY` and starting the connection.

    For more info on the gateway, check out:
    https://discord.com/developers/docs/topics/gateway

    Parameters:
    - client: The bot client user
    - bot_token: The token of the bot
    - intents: Snowflake storing bot intents
    - version?: The version of the gateway being connected to (defaulted to v9)
    """

    def __init__(
        self,
        bot_token: str,
        intents: int = Intents.Standard(),
        version: int = 10,
    ):

        # Client side and connection URL
        self.bot_token = bot_token

        self.wssurl = f"wss://gateway.discord.gg/?v={version}&encoding=json&compress=zlib-stream"
        self.intents = intents
        self.socket: aiohttp.ClientSession = None

        # Gateway events and heartbeats
        self.heartbeat_interval: int = None
        self.opcodes = {
            "DISPATCH": 0,
            "HEARTBEAT": 1,
            "IDENTIFY": 2,
            "PRESENCE UPDATE": 3,
            "VOICE STATE UPDATE": 4,
            "RESUME": 6,
            "RECONNECT": 7,
            "REQUEST GUILD MEMBERS": 8,
            "INVALID socket": 9,
            "HELLO": 10,
            "HEARTBEAT ACK": 11,
        }

        self.identify_req = {
            "op": self.opcodes["IDENTIFY"],
            "d": {
                "token": f"{self.bot_token}",
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "devcord",
                    "$device": "devcord",
                },
            },
        }

        self.jitter = 0.69420
        self.first_heartbeat: bool = True

        # Miscellaneous
        self.zlib_suffix = b"\x00\x00\xff\xff"
        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()

        self.success = Fore.GREEN
        self.fail = Fore.RED

    async def keep_ws_alive(self):
        """
        Keeps the websocket alive by sending heartbeats determined by
        the gateway's `HELLO` response.
        Returns `HEARTBEAT_ACK`s from the gateway when heartbeats are sent.
        """
        while self.socket:
            if isinstance(self.heartbeat_interval, int):
                if self.first_heartbeat is True:
                    await asyncio.sleep(self.heartbeat_interval / 1000 * self.jitter)
                    await self.socket.send_json({
                        "op": 1,
                        "d": self.sequence
                    })
                    self.first_heartbeat = False

                else:
                    await asyncio.sleep(self.heartbeat_interval / 1000)
                    await self.socket.send_json({
                        "op": 1,
                        "d": self.sequence
                    })

    async def listen_to_socket(self):
        """
        Listens to all gateway events and responds to them.
        """
        while self.socket:
            data = await self.socket.receive()
            payload = data.data

            # The below code checks if the gateway sent any events to the user.

            # Closes the websocket if the gateway orders you to cancel it
            if data.type == WSMsgType.CLOSE:
                await self.socket.close()
                code = data.data
                error = data.extra

                # Raises an error if it's not a proper disconnect
                # (https://discord.com/developers/docs/topics/gateway#disconnections)
                if code is not (1000 or 1001):
                    raise GatewayErrors(code, error)

            # Handles any binary response using zlib
            elif data.type == WSMsgType.BINARY:
                self.buffer.extend(payload)

                # Payload compression handling
                if payload[-4:] == self.zlib_suffix:
                    payload = self.inflator.decompress(self.buffer)
                    self.buffer = bytearray()

                # Transport compression handling, in which it uses regular compression,
                # without the extra compression to binary format.
                else:
                    payload = zlib.decompress(payload)

            json_payload = json.loads(payload)

            # Finds the heartbeat_interval and send `IDENTIFY`!
            if json_payload["op"] == self.opcodes["HELLO"]:
                self.heartbeat_interval = json_payload["d"]["heartbeat_interval"]

                await self.socket.send_json(self.identify_req)

            elif json_payload["op"] == self.opcodes["HEARTBEAT ACK"]:
                print("placeholder")

            if json_payload["op"] == self.opcodes["DISPATCH"]:
                self.sequence = json_payload["s"]

            # TODO: Call event listeners when the class BotUser is done

            # Reconnect in case of any errors/gateway demand
            if json_payload["op"] == self.opcodes["RECONNECT"]:
                resume_json = {
                    "op": self.opcodes["RESUME"],
                    "d": {
                        "token": f"{self.bot_token}",
                        # Actually, the socket id is given in the READY message.
                        "socket_id": None,
                        "seq": 1337,
                    },
                }
                await self.socket.send_json(resume_json)

    async def start(self):
        """
        Starts the websocket connecting to the Discord Gateway.
        """

        async with aiohttp.ClientSession() as session:
            if self.socket:
                await self.socket.close()

            self.socket = await session.ws_connect(self.wssurl)

            print(self.success + "Thanks for using devcord! <3")
            print(
                self.success
                + "Want to contribute, view or just star our project? Visit our github! :D"
            )
            print(self.success +
                  "https://github.com/Code-Done-Right/devcord.py" + Fore.RESET)

            # We listen to socket before heartbeat to find heartbeat_interval
            await asyncio.gather(self.listen_to_socket(), self.keep_ws_alive())
