class Intents:
    """
    Calculates the intent value based on the intent(s) chosen.
    This can be specified by the client in the websocket connection,
    or can be only non priviledged (`Standard`) or priviledged intents (`All`).

    As discord recommends it, the standard is to have Non-Priviledged intents unless mentioned.
    (i.e. the `Standard` option.)

    For more information on intents in general, check out:
    https://discord.com/developers/docs/topics/gateway#gateway-intents
    """

    def __init__(self):
        self.INTENTS = {
            "GUILDS": 1 << 0,
            "GUILD_MEMBERS": 1 << 1,
            "GUILD_BANS": 1 << 2,
            "GUILD_EMOJIS_AND_STICKERS": 1 << 3,
            "GUILD_INTEGRATIONS": 1 << 4,
            "GUILD_WEBHOOKS": 1 << 5,
            "GUILD_INVITES": 1 << 6,
            "GUILD_VOICE_STATES": 1 << 7,
            "GUILD_PRESENCES": 1 << 8,
            "GUILD_MESSAGES": 1 << 9,
            "GUILD_MESSAGE_REACTIONS": 1 << 10,
            "GUILD_MESSAGE_TYPING": 1 << 11,
            "DIRECT_MESSAGES": 1 << 12,
            "DIRECT_MESSAGE_REACTIONS": 1 << 13,
            "DIRECT_MESSAGE_TYPING": 1 << 14,
            "GUILD_SCHEDULED_EVENTS": 1 << 16,
        }

    def Standard(self):
        """
        The standard intents, i.e. includes only the non-priviledged intents.
        The only Priviledged intents as of March, 2022 are `GUILD_PRESENCES` and `GUILD_MEMBERS`.
        """
        intent_num = 0
        for key, value in self.INTENTS.items():
            if key != "GUILD_PRESENCES" or "GUILD_MEMBERS":
                intent_num += value

        return intent_num

    def All(self):
        """
        All intents are included with this option.
        """
        intent_num = 0
        for _, value in self.INTENTS.items():
            intent_num += value

        return intent_num
