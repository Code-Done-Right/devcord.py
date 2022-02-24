import devcord
from devcord.command_implements import SlashCommand, PrefixCommand

INTENTS = devcord.intents.All_Enabled()

bot = devcord.BotUser(
        bot_token = '...',
        intents = INTENTS,
        prefixes = ['devcord', 'devcord.']
    )

@bot.command(implements = [SlashCommand, PrefixCommand])
async def ping(ctx):
    await ctx.reply('Pong!')

bot.run()