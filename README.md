# ❓ Devcord

Devcord is a basic Python based Discord API wrapper. The docs, when released, will be linked soon.

Devcord uses Discord's V9 API (The latest API version) and the latest Discord Gateway.

We plan on suppporting Python 3.10, 3.9 and 3.8. However the module might work fine for versions 3.7 and 3.6, although it definitely will be a bit buggy. We recommend you, the user to run it in v3.10 if possible or v3.9.

# 💻 Usage

Devcord is still in very early development stages, but the expected syntax will be updated everytime below:

```py
import devcord
from devcord.command_implements import SlashCommand, PrefixCommand

INTENTS = devcord.Intents.All_Enabled()

bot = devcord.BotUser(
        bot_token = '...',
        prefixes = ['devcord', 'devcord.'],
        intents = INTENTS
    )

@bot.command(implements = [SlashCommand, PrefixCommand])
async def ping(ctx):
    await ctx.reply('Pong!')

bot.run()
```

# ⛓ Links

- (Upcoming) Devcord docs 
- [Discord API documentation](https://discord.com/developers/docs)
- [Discord Server](https://discord.gg/bTnheyspUm)
