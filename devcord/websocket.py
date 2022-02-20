import asyncio
import aiohttp
import platform

class DiscordWebsocket:
    """
    class DiscordWebsocket
    
    A class holding all methods related to the websocket.
    """
    def __init__(self, bot_token: str, intents: int):

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

        self.bot_token = bot_token
        self.intents = intents
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
    
    async def __send_new_hearbeat(self):
        """
        method __send_new_heartbeat
        
        Sends a new hearbeat according to the heartbeat_interval variable.
        This is given in opcode 10's reply from the gateway.
        """
        pass