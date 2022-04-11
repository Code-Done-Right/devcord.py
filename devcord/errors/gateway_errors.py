class GatewayErrors(Exception):
    """
    A class raising errors if an error is returned by the gateway.

    Parameters:
    - code: The status code gvien by the gateway
    - error: any extra errors from the gateway, or anything else
    """

    def __init__(self, code, error):
        print(
            "Oops! An error was raised by the gateway. Visit:\nhttps://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-close-event-codes"
        )

        if code == 4000:
            final = f"ERR {code}\n\nUnknown error\n{error}"

        elif code == 4001:
            final = f"ERR {code}\n\nUnknown Opcode\n{error}"

        elif code == 4002:
            final = f"ERR {code}\n\nDecode Error\n{error}"

        elif code == 4003:
            final = f"ERR {code}\n\nNot authenticated\n{error}"

        elif code == 4004:
            final = f"ERR {code}\n\nAuthentication failed\n{error}"

        elif code == 4005:
            final = f"ERR {code}\n\nAlready authenticated\n{error}"

        elif code == 4007:
            final = f"ERR {code}\n\nInvalid sequence\n{error}"

        elif code == 4008:
            final = f"ERR {code}\n\nRate limited\n{error}"

        elif code == 4009:
            final = f"ERR {code}\n\nSession timed out\n{error}"

        elif code == 4010:
            final = f"ERR {code}\n\nInvalid shard\n{error}"

        elif code == 4011:
            final = f"ERR {code}\n\nSharding required\n{error}"

        elif code == 4012:
            final = f"ERR {code}\n\nInvalid API version\n{error}"

        elif code == 4013:
            final = f"ERR {code}\n\nInvalid Intents\n{error}"

        elif code == 4014:
            final = f"ERR {code}\n\nDisallowed intents\n{error}"

        # Final check (should not run at all)
        else:
            final = "We're confused, we got an error we never got before.\nTry reporting this to our discord server and please paste the error and code. Thanks!"

        super().__init__(final)
