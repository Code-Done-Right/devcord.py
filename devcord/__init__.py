"""
Devcord

An asynchronous, easy to learn Discord API wrapper written in Python v3. We try to make devcord
easy to learn and contribute to!
Check out the github repository for official documentation and a quickstart.
"""
from .intents import Intents

from .errors.general_errors import *
from .errors.gateway_errors import GatewayErrors
from .errors.http_errors import HTTPErrors

from .botuser import BotUser
