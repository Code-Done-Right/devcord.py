import asyncio
import zlib
import platform

import json
import devcord

import aiohttp
from aiohttp.http_websocket import WSMsgType

class DiscordWebSocket:
    """
    class DiscordWebSocket
    
    A class holding all methods related to the websocket.
    """
    def __init__(self, client: 'devcord.BotUser', bot_token: str, intents: int):

        # All possible opcodes
        self.OPCODES = {
            'DISPATCH' : 0,
            'HEARTBEAT' : 1,
            'IDENTIFY': 2,
            'PRESENCE UPDATE': 3,
            'VOICE STATE UPDATE' : 4,
            'RESUME' : 6,
            'RECONNECT': 7,
            'REQUEST GUILD MEMBERS' : 8,
            'INVALID SESSION': 9,
            'HELLO' : 10,
            'HEARTBEAT ACK' : 11
        }

        self.client = client
        self.bot_token = bot_token
        self.intents = intents

        self.heartbeat_interval = None

        self.zlib_suffix = b'\x00\x00\xff\xff'
        self.socket : aiohttp.ClientSession() = None
        self.GATEWAY_URL = 'wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream'

    async def __start_session(self):
        """
        method __start_session

        Initialises a session by sending the IDENTIFY opcode to the Gateway.
        """
        return {
            "op" : self.OPCODES['IDENTIFY'],
            "d" : {
                "bot_token" : self.bot_token,
                "properties" : {
                    "$os" : platform.system(),
                    "$browser" : "devcord",
                    "$device" : "devcord"
                },
                "intents" : self.intents
            }
        }

    async def __keep_alive(self):
        """
        method __keep_alive
        
        Keeps the connection alive by sending heartbeats to the gateway.
        """
        while self.socket:
            await self.socket.send_json(
                json.dumps(
                    {
                        "op" : self.OPCODES['HEARTBEAT']
                    }
                )
            )

            await asyncio.sleep(self.heartbeat_interval / 1000)

    async def listen_ws(self):
        """
        method listen_ws
        
        Listens to the web socket and hears for any opcodes and responds appropriately.
        """
        while self.sock:
            data = await self.socket.receive()
            payload = data.data
            inflator = zlib.decompressobj()

            # Handled when the socket is meant to or forced to close and ran to
            # close the socket properly.
            if data.type == WSMsgType.CLOSE:
                code, message = data.data, data.extra
                
                await self.socket.close()
                
                if code not in (1000, 1001):
                    raise Exception

            # Handles any binary response (not easy to read) and converts to json.
            elif data.type == WSMsgType.BINARY:

                buffer = bytearray()
                buffer.extend(data.data)
                
                if buffer[-4:] == self.zlib_suffix:
                    payload = inflator.decompress(buffer)

                else:
                    payload = zlib.decompress(buffer)


            if data.type in (WSMsgType.BINARY, aiohttp.WSMsgType.TEXT):
                payload_json = json.loads(payload)

                self.sequence = payload_json.get("s")

                # Send identify and set heartbeat
                if payload_json["op"] == self.OPCODES["HELLO"]:
                    self.heartbeat_interval = payload_json["d"]["heartbeat_interval"]

                    identify = self.__start_session()
                    await self.socket.send_json(identify)

                # Call event handlers
                elif payload_json["op"] == self.OPCODES["DISPATCH"]:
                    if payload_json["t"] == "READY":
                        self.session_id = payload_json["d"]["session_id"]

                    await self.client.call_event_handler(payload_json["t"], payload_json["d"])

                # Reconnect
                elif payload_json["op"] == self.OPCODES["RECONNECT"]:
                    await self.sock.close()
                    await self.start()
    
    async def setup(self):
        """
        method setup
        
        Final setup of the websocket.
        """
        async with aiohttp.ClientSession() as session:

            self.socket = await session.ws_connect(self.GATEWAY_URL)

            await asyncio.gather(
                self.listen_ws(),
                self.__keep_alive()
            )