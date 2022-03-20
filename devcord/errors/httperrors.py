class HTTPErrors(Exception):
    def __init__(self, code):
        # This is easy to implement but this will probably be unused until the
        # below TODO is done.
        #
        # TODO:
        # https://discord.com/developers/docs/topics/opcodes-and-status-codes#http
        # Code a system to filter through the above errors.
        pass
