from .handler import Handler
from commands import *
from config import config

class LinuxHandler(Handler):
    def __init__(self, command, args):
        super().__init__(command, args)

    #####

    def build(self):
        tests_active = "-DTESTS=ON" if self.tests else ""
        CreateDirectoryCommand(self.build_folder).execute()

        Command.executeCommands([
            Command("CXX={} cd _build_linux && cmake -G Ninja {} ..".format(config.cxx_compiler, tests_active), stdout=True),
            Command("cd _build_linux && ninja"),
        ])

    def execute(self):
        game_dir = "tests" if self.tests else "game"
        debug_cmd = "{} ".format(config.debugger) if self.debug else ""

        Command.executeCommands([
            CopyDirectoryCommand("engine/assets", "_build_linux/{}/assets".format(game_dir)),
            CopyDirectoryCommand("{}/assets".format(game_dir), "_build_linux/{}/assets".format(game_dir)),
            Command("cd _build_linux/{dir} && {cmd}./{dir}".format(cmd=debug_cmd, dir=game_dir)),
        ])

    def dep_build(self):
        pass

    def package(self):
        pass
