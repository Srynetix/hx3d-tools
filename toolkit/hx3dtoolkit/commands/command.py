from hx3dtoolkit.config import config
from hx3dtoolkit.utils.color_print import color_print as cprint
import os
import sys

from colorama import Fore

class Command:
    def __init__(self, command, **options):
        self.command = command
        self.options = options

    def execute(self):
        return self.__class__.executeRawCommand(self.command, **self.options)

    @staticmethod
    def executeCommands(commands):
        for command in commands:
            if command.execute() != 0:
                cprint("> Error", color=Fore.RED)
                sys.exit()

    @staticmethod
    def executeRawCommand(command, stderr=True, stdout=False):
        if not stderr and not stdout and not config.debug_mode:
            command += " &> /dev/null"
        elif not stderr:
            command += " 2> /dev/null"
        elif not stdout and not config.debug_mode:
            command += " > /dev/null"

        if config.debug_mode:
            print("[D] Executing `{}`".format(command))

        code = os.system(command)
        if code != 0 and stderr:
            cprint("- Error Code: {}".format(code), color=Fore.RED)
            return code
        return 0
