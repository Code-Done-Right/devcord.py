"""
Devcord

Devcord is an asynchronous programming-based module that uses aiohttp to make bots.
We aim to make using and contributing to devcord as easy as humanly possible, while
keeping necessary complexity. Thanks for using devcord! <3 

Example usage:

```py
import devcord

bot = devcord.BotUser(
    bot_token = "...",
    intents = devcord.Intents.Standard(),
    version = 10,
    prefixes = ["devcord."],
)

bot.run()
```
"""

from .internals.intents import Intents

from .errors.generalerr import InterruptionError, BaseError
from .errors.apierr import InvalidRequest

from .botuser import BotUser
