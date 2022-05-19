# ❓ Devcord

Devcord is a Python based Discord API wrapper. We use Discord's V10 API (The latest API version) and the latest Discord Gateway.

We are still in the alpha stages of development.

Devcord is well-tested on Python v3.10, but ideally v3.9 and v3.8 should work with equal performance.

# 💻 Usage

Devcord is still in very early development stages, but the expected syntax will be updated everytime below:

```py
import devcord

INTENTS = devcord.Intents.All()

bot = devcord.BotUser(
        bot_token = '...',
        intents = INTENTS,
        prefixes = ['devcord', 'devcord.']
    )

bot.run()
```

# ⛓ Links

- (Upcoming) Devcord docs
- [Discord API documentation](https://discord.com/developers/docs)
- [Discord Server](https://discord.gg/bTnheyspUm)
