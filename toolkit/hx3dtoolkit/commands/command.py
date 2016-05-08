from hx3dtoolkit.config import config
import os

class Command:
    def __init__(self, command, **options):
        self.command = command
        self.options = options

    def execute(self):
        self.__class__.executeRawCommand(self.command, **self.options)

    @staticmethod
    def executeCommands(commands):
        for command in commands:
            command.execute()

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
            print("- Error Code: ", code)
