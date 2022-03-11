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

    def __init__(self, client, bot_token: str, intents: int, version: int = 9):

        # Client side and connection URL
        self.client = client
        self.bot_token = bot_token
        self.WSSGATEWAYURL = f"wss://gateway.discord.gg/?v={version}&encoding=json"
        self.intents = intents

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
            "INVALID SESSION": 9,
            "HELLO": 10,
            "HEARTBEAT ACK": 11
        }
