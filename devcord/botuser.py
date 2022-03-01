import asyncio
import aiohttp

from intents import Intents

class BotUser:
    def __init__(self, bot_token, intents = Intents.Standard, prefixes = None):
        self.bot_token = bot_token
        self.intents = intents
        self.prefixes = prefixes
        self.API_URL = f'https://discord.com/api/v9'

        self.http_connection = None

    # I have no freaking clue, I will get back with this
    
    # async def __create_new_command(self, connection):
    #     async with aiohttp.ClientSession as session:
    #         data = {

    #         }
    #         session.post()

    async def run(self):
        """
        method run
        
        Runs the bot.
        """
        pass