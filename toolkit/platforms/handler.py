from dependencies.colorama import Fore, Style
from utils import color_print
from commands import *

class Handler:
    def __init__(self, command, args):
        self.command = command
        self.args = args
        self.platform = args.platform[0] if isinstance(args.platform, list) else args.platform

        self.tests = "tests" in self.args and self.args.tests
        self.debug = "debug" in self.args and self.args.debug

    def handle(self):
        test_mode = " (test mode)" if self.tests else ""
        debug_mode = " (w/ debug)" if self.debug else ""
        platform = "all" if self.platform is None else self.platform

        if self.command == "build":
            color_print("> Building for {}{}...".format(platform, test_mode))
            self.build()
        elif self.command == "generate":
            self.generate()
        elif self.command == "clean":
            color_print("> Cleaning for {}...".format(platform))
            self.clean()
        elif self.command == "execute":
            color_print("> Executing for {}{}{}...".format(platform, test_mode, debug_mode))
            self.execute()
        elif self.command == "package":
            self.package()
        elif self.command == "dep-fetch":
            self.dep_fetch()
        else:
            raise NotImplementedError("No such command: {}".format(self.command))

    @property
    def build_folder(self):
        return "_build_{}".format(self.platform)

    ##########

    def build(self):
        raise NotImplementedError("You can't build for platform {}".format(self.platform))

    def generate(self):
        raise NotImplementedError("You can't generate for platform {}".format(self.platform))

    def clean(self):
        Command("rm -r {}".format(self.build_folder), stderr=False).execute()

    def execute(self):
        raise NotImplementedError("You can't execute for platform {}".format(self.platform))

    def package(self):
        raise NotImplementedError("You can't package for platform {}".format(self.platform))

    def dep_fetch(self):
        raise NotImplementedError("You can't fetch dependencies for platform {}".format(self.platform))
