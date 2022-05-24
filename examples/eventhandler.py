import devcord
from devcord.events import MessageCreate
from devcord import BotUser

bot = BotUser(
    bot_token="OTcwMzE5MDEyMDE1ODAwNDIx.Ym6OAA.O3xJJiTCAZxFeehnQ2Pks6wj4lU",
    intents=devcord.Intents.All(),
    version=10,
    prefixes=["devcord."]
)


@bot.event(event=MessageCreate)
async def ping(ctx):
    ctx.respond("pong!")

bot.run()
