# Imports
import devcord
from devcord import HTTPConnection, GatewayWebSocket


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

    def __init__(self, bot_token, intents=devcord.Intents.Standard(), prefixes=None):
        self.bot_token = bot_token
        self.intents = intents
        self.prefixes = prefixes
