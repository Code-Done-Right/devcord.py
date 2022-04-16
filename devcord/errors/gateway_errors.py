"""
A module storing all documented gateway errors.
"""
from colorama import Fore


class GatewayErrors(Exception):
    """
    A class raising errors if an error is returned by the gateway.

    Parameters:
    - code: The status code gvien by the gateway
    - error: any extra errors from the gateway, or anything else
    """

    def __init__(self, code, error):
        print(
            Fore.RED + "Oops! An error was raised by the gateway." + Fore.RESET
        )
        print(Fore.RED + "Visit:\nhttps://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-close-event-codes" + Fore.RESET)

        if code == 4000:
            final = f"\n ERR {code}\n\nUnknown error\n{error}"

        elif code == 4001:
            final = f"\n ERR {code}\n\nUnknown Opcode\n{error}"

        elif code == 4002:
            final = f"\n ERR {code}\n\nDecode Error\n{error}"

        elif code == 4003:
            final = f"\n ERR {code}\n\nNot authenticated\n{error}"

        elif code == 4004:
            final = f"\n ERR {code}\n\nAuthentication failed\n{error}"

        elif code == 4005:
            final = f"\n ERR {code}\n\nAlready authenticated\n{error}"

        elif code == 4007:
            final = f"\n ERR {code}\n\nInvalid sequence\n{error}"

        elif code == 4008:
            final = f"\n ERR {code}\n\nRate limited\n{error}"

        elif code == 4009:
            final = f"\n ERR {code}\n\nSession timed out\n{error}"

        elif code == 4010:
            final = f"\n ERR {code}\n\nInvalid shard\n{error}"

        elif code == 4011:
            final = f"\n ERR {code}\n\nSharding required\n{error}"

        elif code == 4012:
            final = f"\n ERR {code}\n\nInvalid API version\n{error}"

        elif code in (4013, 4014):
            final = f"\n ERR {code}\n\nInvalid or Disallowed Intents\n{error}"

        # Final check (should not run at all)
        else:
            final = "We're confused, we got an error we never got before.\nTry reporting this \
            to our discord server. Thanks!"

        super().__init__(Fore.RED + final + Fore.RESET)
