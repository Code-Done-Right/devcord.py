"""
Submodule holding classes representing gateway events.
See:
https://discord.com/developers/docs/topics/gateway#commands-and-events

These classes are handled by the BotUser instance when the `BotUser.event` is decorated
over a function, which further handles all responses.

See devcord documentation for more info on individual classes.
"""
from .message import MessageCreate
