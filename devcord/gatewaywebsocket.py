# Imports
import aiohttp
from aiohttp import WSMsgType
import asyncio
from devcord import Intents, GatewayErrors

import zlib
import datetime
import json
from colorama import Fore


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

        self.WSSGATEWAYURL = f"wss://gateway.discord.gg/?v={version}&encoding=json&compress=zlib-stream"
        self.intents = intents
        self.socket: aiohttp.ClientSession = None

        # Gateway events and heartbeats
        self.heartbeat_interval: int = None
        self.OPCODES = {
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

        self.IDENTIFY_REQ = {
            "op": self.OPCODES["IDENTIFY"],
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

        self.first_heartbeat = True
        self.JITTER = 0.2

        # Miscellaneous
        self.ZLIB_SUFFIX = b"\x00\x00\xff\xff"
        self.BUFFER = bytearray()
        self.INFLATOR = zlib.decompressobj()

        self.SUCCESS = Fore.GREEN
        self.FAIL = Fore.RED

    async def keep_ws_alive(self):
        """
        Keeps the websocket alive by sending heartbeats determined by
        the gateway's `HELLO` response.
        Returns `HEARTBEAT_ACK`s from the gateway when heartbeats are sent.
        """
        while self.socket:
            if type(self.heartbeat_interval) == int:
                if self.first_heartbeat == True:
                    # Ran only if this is the first heartbeat
                    await asyncio.sleep(self.heartbeat_interval * 1000 * self.JITTER)

                    await self.socket.send_json({"op": self.OPCODES["HEARTBEAT"]})
                    self.first_heartbeat = False

                else:
                    # Ran only if this is not first heartbeat interval
                    await asyncio.sleep(self.heartbeat_interval * 1000)

                    await self.socket.send_json({"op": self.OPCODES["HEARTBEAT"]})

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
                self.BUFFER.extend(payload)

                # Payload compression handling
                if payload[-4:] == self.ZLIB_SUFFIX:
                    payload = self.INFLATOR.decompress(self.BUFFER)
                    self.BUFFER = bytearray()

                # Transport compression handling, in which it uses regular compression,
                # without the extra compression to binary format.
                else:
                    payload = zlib.decompress(payload)

            json_payload = json.loads(payload)

            # Finds the heartbeat_interval and send `IDENTIFY`!
            if json_payload["op"] == self.OPCODES["HELLO"]:
                self.heartbeat_interval = json_payload["d"]["heartbeat_interval"]

                await self.socket.send_json(self.IDENTIFY_REQ)

            elif json_payload["op"] == self.OPCODES["HEARTBEAT ACK"]:
                print("placeholder")

            # TODO: Call event listeners when the class BotUser is done

            # Reconnect in case of any errors/gateway demand
            if json_payload["op"] == self.OPCODES["RECONNECT"]:
                resume_json = {
                    "op": self.OPCODES["RESUME"],
                    "d": {
                        "token": f"{self.bot_token}",
                        "socket_id": self.socket_id,
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

            self.socket = await session.ws_connect(self.WSSGATEWAYURL)

            print(self.SUCCESS + "Thanks for using devcord! <3")
            print(
                self.SUCCESS
                + "Want to contribute, view or just star our project? Visit our github! :D"
            )
            print(self.SUCCESS +
                  "https://github.com/Code-Done-Right/devcord.py" + Fore.RESET)
            print(self.SUCCESS + "Tip: Focus on the red text if any errors come, and don't forget to report to our discord!" + Fore.RESET)

            # We listen to socket before heartbeat to find heartbeat_interval
            await asyncio.gather(self.listen_to_socket(), self.keep_ws_alive())
