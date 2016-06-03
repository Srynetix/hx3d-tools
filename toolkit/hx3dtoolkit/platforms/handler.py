from colorama import Fore, Style

from hx3dtoolkit.utils.color_print import color_print
from hx3dtoolkit.commands import *
from hx3dtoolkit.utils.dependency_fetch import get_fetch_folder
from hx3dtoolkit.config import config

from functools import reduce
import os

class Handler:
    def __init__(self, command, args):
        self.command = command
        self.args = args
        self.platform = None if not hasattr(args, "platform") else args.platform[0] if isinstance(args.platform, list) else args.platform

        self.tests = "tests" in self.args and self.args.tests
        self.debug = "debug" in self.args and self.args.debug
        self.memcheck = "memcheck" in self.args and self.args.memcheck

    def handle(self):
        test_mode = " (test mode)" if self.tests else ""
        debug_mode = " (w/ debug)" if self.debug else ""
        memcheck_mode = " (w/ memcheck)" if self.memcheck else ""
        platform = "all" if self.platform is None else self.platform

        if self.command == "build":
            if self.args.clean:
                color_print("> Cleaning for {}{}...".format(platform, test_mode), color=Fore.YELLOW)
                self.clean()
            color_print("> Building for {}{}...".format(platform, test_mode), color=Fore.YELLOW)
            self.build()
            if self.args.execute:
                color_print("> Executing for {}{}{}...".format(platform, test_mode, debug_mode or memcheck_mode), color=Fore.YELLOW)
                self.execute()
        elif self.command == "generate":
            self.generate()
        elif self.command == "clean":
            color_print("> Cleaning for {}...".format(platform), color=Fore.YELLOW)
            self.clean()
        elif self.command == "execute":
            color_print("> Executing for {}{}{}...".format(platform, test_mode, debug_mode or memcheck_mode), color=Fore.YELLOW)
            self.execute()
        elif self.command == "package":
            self.package()
        elif self.command == "dep-fetch":
            color_print("> Fetching dependencies for {}...".format(platform), color=Fore.YELLOW)
            self.dep_fetch()
        elif self.command == "doc":
            color_print("> Building documentation...", color=Fore.YELLOW)
            self.doc()
        else:
            raise NotImplementedError("No such command: {}".format(self.command))

    @property
    def build_folder(self):
        return "_build_{}".format(self.platform)

    def check_for_build_folder(self):
        if not os.path.exists(self.build_folder):
            color_print("> Build folder does not exists. Prepare to build...", color=Fore.RED)

            test_mode = " (test mode)" if self.tests else ""
            color_print("> Building for {}{}...".format(self.platform, test_mode), color=Fore.YELLOW)
            self.build()

    def get_providers_command(self):
        providers = {
            "AUDIO_PROVIDER": config.providers.audio,
            "WINDOW_PROVIDER": config.providers.window
        }

        return reduce(lambda acc, item: acc + "-D{}={} ".format(item[0], item[1]), providers.items(), "")

    ##########

    def build(self):
        raise NotImplementedError("You can't build for platform {}".format(self.platform))

    def generate(self):
        from platforms.generator import generate
        generate(self.args)

    def clean(self):
        Command("rm -r {}".format(self.build_folder), stderr=False).execute()

    def execute(self):
        raise NotImplementedError("You can't execute for platform {}".format(self.platform))

    def package(self):
        raise NotImplementedError("You can't package for platform {}".format(self.platform))

    def dep_fetch(self):
        fetch_folder = get_fetch_folder(self.platform)
        build_folder = "{}/build".format(fetch_folder)

        Command.executeCommands([
            RemoveDirectoryCommand(fetch_folder),
            CreateDirectoryCommand(fetch_folder),

            CreateDirectoryCommand(build_folder),
            CreateDirectoryCommand("{}/lib".format(build_folder)),
            CreateDirectoryCommand("{}/include".format(build_folder)),
        ])
