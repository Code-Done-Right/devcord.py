# Imports
import aiohttp
import asyncio
from devcord import Intents

import zlib
import datetime
import json


class GatewayWebSocket:
    """
    A class creating the Gateway websocket. Handles all gateway events such as
    opcodes, heartbeats and ACKs, etc.

    Starts with sending `IDENTIFY` and starting the connection.

    For more info on the gateway, check out:
    https://discord.com/developers/docs/topics/gateway

    Parameters:
    - client - The bot client user
    - bot_token - The token of the bot
    - intents - Snowflake storing bot intents
    - version? - The version of the gateway being connected to (defaulted to v9)
    """

    def __init__(self, client, bot_token: str, intents: int = Intents.Standard(), version: int = 9):

        # Client side and connection URL
        self.client = client
        self.bot_token = bot_token

        self.WSSGATEWAYURL = f"wss://gateway.discord.gg/?v={version}&encoding=json"
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
            "HEARTBEAT ACK": 11
        }

        # Miscellaneous
        self.ZLIB_SUFFIX = b'\x00\x00\xff\xff'
        self.BUFFER = bytearray()
        self.INFLATOR = zlib.decompressobj()

    async def identify_request(self):
        """
        Sends an `IDENTIFY` packet to the gateway to start the connection.
        Occurs whenever you want to start a new session or reconnect the socket after
        a sudden non-graceful closing of the connection.
        """
        return {
            "op": self.OPCODES["IDENTIFY"],
            "d": {
                "token": f"{self.bot_token}",
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "devcord",
                    "$device": "devcord"
                }
            }
        }

    async def send_new_heartbeat(self, socket: aiohttp.ClientWebSocketResponse):
        """
        Sends a new heartbeat accoding to the heartbeat_interval given
        in the `HELLO` packet.

        Parameters:
            - socket (`aiohttp.ClientWebSocketResponse`): Socket for sending the heartbeat.

        """
        if not socket.closed:
            await socket.send_json({
                "op": self.OPCODES["HEARTBEAT"]
            })

    async def keep_ws_alive(self):
        """
        Keeps the websocket alive by sending heartbeats determined by
        the gateway's `HELLO` response.
        Returns `HEARTBEAT_ACK`s from the gateway when heartbeats are sent.
        """
        while self.socket:
            if self.heartbeat_interval:
                # Ran only if heartbeat_interval exists AND session exists
                await asyncio.sleep(self.heartbeat_interval * 1000)

                await self.send_new_heartbeat(self.socket)

    async def listen_to_socket(self):
        """
        Listens to all gateway events and responds to them.
        """
        while self.socket:
            data = self.socket.receive()
            payload = data.data()

            # The below code checks if the gateway sent any events to the user.

            # Closes the websocket if the gateway orders you to cancel it
            if data.type == aiohttp.WSMsgType.CLOSE:
                await self.socket.close()
                code = data.data

                # Raises an error if it's not a proper disconnect
                # (https://discord.com/developers/docs/topics/gateway#disconnections)
                if code is not (1000 or 1001):
                    raise Exception

            # Handles any binary response using zlib
            elif data.type == aiohttp.WSMsgType.BINARY:
                self.BUFFER.extend(data)

                # Payload compression handling
                if data[-4:] == self.ZLIB_SUFFIX:
                    data = self.INFLATOR.decompress()

                # Transport compression handling, in which it uses regular compression,
                # without the extra compression to binary format.
                else:
                    data = zlib.decompress(data)

            if data.type == aiohttp.WSMsgType.TEXT or aiohttp.WSMsgType.BINARY:
                json_payload = json.loads(payload)

                # Finds the heartbeat_interval and send `IDENTIFY`!
                if json_payload["op"] == self.OPCODES["HELLO"]:
                    self.heartbeat_interval = json_payload["d"]["heartbeat_interval"]

                    identify_json = self.identify_request()
                    await self.socket.send_json(identify_json)

                # Handles `READY` response
                if json_payload["op"] == self.OPCODES["READY"]:
                    self.socket_id = json_payload["socket_id"]

                # Reconnect in case of any errors/gateway demand
                if json_payload["op"] == self.OPCODES["RECONNECT"]:
                    resume_json = {
                        "op": self.OPCODES["RESUME"],
                        "d": {
                            "token": f"{self.bot_token}",
                            "socket_id": self.socket_id,
                            "seq": 1337
                        }
                    }
                    await self.socket.send_json(resume_json)

    async def start(self):
        """
        Starts the websocket connecting to the Discord Gateway.
        """
        async with aiohttp.ClientSession as session:
            self.socket = await session.ws_connect(self.WSSGATEWAYURL)

            # We listen to socket before heartbeat to find heartbeat_interval
            await asyncio.gather(
                self.listen_to_socket(),
                self.keep_ws_alive
            )
