"""
Module controlling the WebSocket connecting to the Gateway.
"""

import asyncio
import json
from rich import print

import typing
from typing import Optional
import zlib

import aiohttp
from aiohttp import ClientSession, WSMsgType
from devcord import Intents
from devcord.internals.apiconnection import APIConnection


__all__ = [
    "GatewayWebSocket"
]


class GatewayWebSocket:
    """
    Creates and handles a WebSocket connection to the Gateway. Handles
    and listens to all events from Discord, via `DISPATCH` payloads.

    Refer to the gateway here:
    https://discord.com/developers/docs/topics/gateway

    Parameters:
    - bot_token: The token of the bot.
    - intents?: The intents enabled and requested to the Gateway.
    - version?: The gateway version
    """

    def __init__(
        self,
        api: APIConnection,
        bot_token: Optional[str],
        intents: Optional[int],
        version: Optional[int] = 10
    ):
        # Client side
        self.api = api
        self.token = bot_token
        self.intents = intents
        self.gatewaywssurl = f"wss://gateway.discord.gg/?v={version}&encoding=json&compress=zlib-stream"
        self.session: aiohttp.ClientSession = None
        self.session_id: str = None
        self.socket: aiohttp.ClientWebSocketResponse = None
        self.sequence: int = None

        # Compression
        self.zlib_suffix = b'\x00\x00\xff\xff'
        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()

        # Misc
        self.opcodes = {
            "DISPATCH":                0,
            "HEARTBEAT":               1,
            "IDENTIFY":                2,
            "PRESENCE UPDATE":         3,
            "VOICE STATE UPDATE":      4,
            "RESUME":                  6,
            "RECONNECT":               7,
            "REQUEST GUILD MEMBERS":   8,
            "INVALID SESSION":         9,
            "HELLO":                   10,
            "HEARTBEAT ACK":           11
        }
        self.heartbeat_interval: int = 41250
        # I am setting the heartbeat interval, because if for some reason a delay happens
        # while Discord gives the heartbeat interval, it will raise an exception.
        self.first: bool = True

    async def __send_identify_packet(self):
        """
        Sends an `IDENTIFY` packet to the gateway after connecting and receiving a `HELLO`.
        """
        await self.socket.send_json(
            {
                "op": 2,
                "d": {
                    "token": f"{self.token}",
                    "intents": self.intents,
                    "properties": {
                        "$os": "linux",
                        "$browser": "devcord",
                        "$device": "devcord"
                    }
                }
            }
        )

    async def __keep_conn_alive(self):
        while self.socket:
            heartbeat = {
                "op": 1,
                "d": self.sequence
            }
            if type(self.heartbeat_interval) == int and self.first == True:
                await asyncio.sleep(self.heartbeat_interval / 1000 * 0.5)
                await self.socket.send_json(heartbeat)
                # 0.5 is the jitter
                self.first = False

            else:
                await asyncio.sleep(self.heartbeat_interval / 1000)
                await self.socket.send_json(heartbeat)

    async def __listen_to_socket(self):
        """
        Listens to the WebSocket for messages such as events, CLOSE messages, etc
        and handles them appropriately.
        """
        while self.socket:
            payload = await self.socket.receive()
            json_payload = payload.data

            # Closes the connection if the gateway tells us to do so.
            if payload.type == WSMsgType.CLOSE:
                await self.socket.close()

            # Handles `WSMsgType.BINARY` type compressed payloads.
            if payload.type == WSMsgType.BINARY:
                self.buffer.extend(json_payload)

                if json_payload[-4:] == self.zlib_suffix:

                    json_payload = self.inflator.decompress(self.buffer)
                    self.buffer = bytearray()
                    json_payload = json.loads(json_payload)

            # Handles the JSON payload!
            if payload.type in (WSMsgType.BINARY, WSMsgType.TEXT):
                if json_payload["op"] == self.opcodes["HELLO"]:
                    self.heartbeat_interval = json_payload["d"]["heartbeat_interval"]
                    await self.__send_identify_packet()

                if json_payload["op"] == self.opcodes["DISPATCH"]:
                    self.sequence = json_payload["s"]

                    if json_payload["t"] == "MESSAGE_CREATE":
                        if json_payload["d"]["content"] == "hello":
                            await self.api.request("POST", "/channels/969944742584549430/messages", payload={"content": "It works, finally!"})

    async def start_websocket(self):
        """
        Starts the WebSocket!
        """
        if self.session:
            await self.session.close()

        async with aiohttp.ClientSession() as self.session:
            self.socket = await self.session.ws_connect(self.gatewaywssurl)
            print(
                "[sea_green2]:D[/sea_green2] [green1]Connected to the Gateway.[/green1]")
            await asyncio.gather(self.__listen_to_socket(), self.__keep_conn_alive())
