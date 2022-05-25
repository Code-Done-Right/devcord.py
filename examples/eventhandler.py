import devcord
from devcord.events import MessageCreate
from devcord import BotUser

bot = BotUser(
    bot_token="...",
    intents=devcord.Intents.All(),
    version=10,
    prefixes=["devcord."]
)


@bot.event(event=MessageCreate)
async def ping(ctx):
    ctx.respond("pong!")

bot.run()
