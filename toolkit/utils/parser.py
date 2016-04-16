import argparse

####
#
# hx3d toolkit
#
# - build => build the engine / game / tests for one platform
# - generate => generate a new game to a directory
# - clean => clean a build for one platform
# - execute => execute the game / tests for one platform (--tests)
# - package => package the game / tests for one platform
# - dep-fetch => fetch the dependencies for one platform
#
# => One parser config file by platform

from utils.color_print import color_print
from dependencies.colorama import Fore, Style
from platforms.main_handler import MainHandler
from platform import PLATFORMS

class Parser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='hx3d toolkit - simple game framework')
        self.subparsers_handler = self.parser.add_subparsers(dest='command')
        self.subparsers_handler.required = True

        # Build
        self.subparser_build = self.subparsers_handler.add_parser("build", help="Build the game for one platform")
        self.subparser_build.add_argument("platform", nargs=1, help="Platform type", choices=PLATFORMS.keys())
        self.subparser_build.add_argument("-t", "--tests", action="store_true", help="Build tests")

        # Clean
        self.subparser_clean = self.subparsers_handler.add_parser("clean", help="Clean a build for one platform")
        self.subparser_clean.add_argument("platform", nargs="?", help="Platform type", choices=PLATFORMS.keys())

        # Execute
        self.subparser_execute = self.subparsers_handler.add_parser("execute", help="Execute the game (or tests) for one platform")
        self.subparser_execute.add_argument("platform", nargs=1, help="Platform type", choices=PLATFORMS.keys())
        self.subparser_execute.add_argument("-t", "--tests", action="store_true", help="Execute tests")
        self.subparser_execute.add_argument("-d", "--debug", action="store_true", help="Debug the executable")

        # Package
        self.subparser_package = self.subparsers_handler.add_parser("package", help="Package the game (or tests) for one platform")
        self.subparser_package.add_argument("platform", nargs=1, help="Platform type", choices=PLATFORMS.keys())
        self.subparser_package.add_argument("-t", "--tests", action="store_true", help="Package tests")

        # Generate
        self.subparser_generate = self.subparsers_handler.add_parser("generate", help="Generate a new game project")
        self.subparser_generate.add_argument("name", nargs=1, help="Game name")
        self.subparser_generate.add_argument("directory", nargs=1, help="Game directory")
        self.subparser_generate.add_argument("package_name", nargs=1, help="Package name")

        # Dep-fetch
        self.subparser_depfetch = self.subparsers_handler.add_parser("dep-fetch", help="Fetch dependencies for one platform")
        self.subparser_depfetch.add_argument("platform", nargs=1, help="Platform type", choices=PLATFORMS.keys())

        self.parse_args()

    def parse_args(self):
        args = self.parser.parse_args()
        command = args.command
        platform = args.platform[0] if isinstance(args.platform, list) else args.platform

        color_print("\nhx3d toolkit -- let's start !\n", color=Fore.CYAN)

        if platform is None:
            MainHandler(command, args).handle()
        elif platform in PLATFORMS:
            PLATFORMS[platform](command, args).handle()
        else:
            color_print("> Bad platform ({})".format(platform), color=Fore.RED)

        color_print("> Done.")
