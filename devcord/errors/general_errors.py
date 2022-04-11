# Imports
from colorama import Fore


class InterruptError(Exception):
    """
    Raises an error for any general interruption while the code is running.
    """

    def __init__(self, *, error_type) -> None:
        error = None
        if error_type == KeyboardInterrupt:
            error = Fore.YELLOW + \
                "\n InterruptError \n\n A KeyBoardInterrupt happened during the execution of the code." + Fore.RESET

        else:
            error = Fore.RED + "InterruptError \n\n We don't know what this error is. Maybe, try reporting to our github or discord?" + Fore.RESET

        super().__init__(error)


class InvalidSessionError(Exception):
    """
    Raises an error whenever some login credentials (user agent, bot token, etc) is invalid.
    """

    def __init__(self, err_type):

        error = None
        if err_type == "bot_token":
            error = Fore.RED + "\n InvalidSessionError \n\n Your bot token is invalid. It does not work for logging into your bot. Regenerate your token and paste a new one here."

        else:
            error = Fore.RED + "Other cases will be handled later :P"

        super().__init__(error)
