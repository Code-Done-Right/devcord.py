import devcord

class Intents:
    """
    class Intents
    
    Returns all intents, standard or all intents.
    """
    GUILDS = (1 << 0)
    GUILD_MEMBERS = (1 << 1)
    GUILD_BANS = (1 << 2)
    GUILD_EMOJIS_AND_STICKERS = (1 << 3)
    GUILD_INTEGRATIONS = (1 << 4)
    GUILD_WEBHOOKS = (1 << 5)
    GUILD_INVITES = (1 << 6)
    GUILD_VOICE_STATES = (1 << 7)
    GUILD_PRESENCES = (1 << 8)
    GUILD_MESSAGES = (1 << 9)
    GUILD_MESSAGE_REACTIONS = (1 << 10)
    GUILD_MESSAGE_TYPING = (1 << 11)
    DIRECT_MESSAGES = (1 << 12)
    DIRECT_MESSAGE_REACTIONS = (1 << 13)
    DIRECT_MESSAGE_TYPING = (1 << 14)
    GUILD_SCHEDULED_EVENTS = (1 << 16)
        
    @classmethod
    def All_Enabled(cls):
        """
        method All_Enabled

        All registered intents, including privileged ones.
        """
        return cls.merge_intents(cls, True)

    @classmethod
    def Standard(cls):
        """
        method Standard

        Returns all non-privileged intents.
        """
        return cls.merge_intents(cls, False)

    @classmethod
    def merge_intents(cls, intent_list, privileged: bool = False):
        """
        Convert a list of intents into a number.
        
        Parameters:
        - intent_list: A list of intents.
        - privileged (bool): Whether or not to include privileged intents in the result.
        """

        result = 0
        for value in intent_list:
            if not privileged and value in (devcord.Intents.GUILD_MEMBERS, devcord.Intents.GUILD_PRESENCES):
                continue
            result = result | value.value
        return result