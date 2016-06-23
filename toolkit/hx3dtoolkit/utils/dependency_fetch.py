# Dependency fetch

from hx3dtoolkit.commands import *
from hx3dtoolkit.config import config
from hx3dtoolkit.utils.color_print import color_print as cprint

from colorama import Fore, Style
from contextlib import contextmanager
import sys
import os

class DepFetcher():
    DEPENDENCY_FILE = "dependencies.yaml"

    def __init__(self, handler):
        self.handler = handler

    @property
    def fetch_folder(self):
        platform = self.handler.platform or "common"
        return "_dep_fetch_{}".format(platform)

    @property
    def build_folder(self):
        platform = self.handler.platform or "common"
        return "{}/build".format(self.fetch_folder)

    def get_lib_folder(self, library_name):
        library = self.get_library(library_name)
        return "{}/{}".format(self.fetch_folder, library["folder"])

    def get_library(self, library_name):
        if library_name in config.dependencies:
            return config.dependencies[library_name]
        else:
            cprint("  Library `` does not exist.".format(library_name), color=Fore.RED)
            sys.exit(1)

    def download(self, library_name):
        library = self.get_library(library_name)
        url = library["url"]
        filename = library["filename"]

        if config.debug_mode:
            cprint("  - Downloading `{}` ({})".format(library_name, filename))

        Command("cd {} && curl --progress-bar {} -o {}".format(self.fetch_folder, url, filename)).execute()

    def extract(self, library_name):
        library = self.get_library(library_name)
        filename = library["filename"]
        extension = library["extension"]
        folder = self.fetch_folder

        if config.debug_mode:
            cprint("  - Extracting `{}`".format(filename))

        if extension == "tar.gz":
            Command("cd {} && tar -xf {}".format(folder, filename)).execute()
        elif extension == "zip":
            Command("cd {} && unzip -q {}".format(folder, filename)).execute()
        else:
            cprint("    /!\\ Unsupported type: {}".format(extension), color=Fore.RED)
            sys.exit(1)

    def execute_commands(self, library_name, commands):
        for command in commands:
            self.execute_in_folder(library_name, command)

    def apply_injections(self, library_name):
        library = self.get_library(library_name)
        if not "injections" in library:
            if config.debug_mode:
                cprint("  - No injections for {}".format(library_name))
        else:
            injections = library["injections"]
            for injection in injections:
                if config.debug_mode:
                    cprint("  - Injecting file `{}` for `{}`".format(injection["name"], library_name))

                filename = injection["filename"]
                src = injection["src"]
                dst = injection["dst"]
                current_folder = self.pop_last_dirname(os.path.dirname(os.path.realpath(__file__)))

                Command("cp {}/assets/patches/{}/{}/{} {}/{}/".format(
                    current_folder,
                    library_name,
                    src,
                    filename,
                    self.get_lib_folder(library_name),
                    dst
                )).execute()

    def apply_patches(self, library_name):
        library = self.get_library(library_name)
        if not "patches" in library:
            if config.debug_mode:
                cprint("  - No patches for {}".format(library_name))
        else:
            patches = library["patches"]
            for patch in patches:
                if config.debug_mode:
                    cprint("  - Applying patch `{}`".format(patch["name"]))

                filename = patch["filename"]
                src = patch["src"]
                dst = patch["dst"]
                current_folder = self.pop_last_dirname(os.path.dirname(os.path.realpath(__file__)))

                Command("cp {}/assets/patches/{}/{}/{} {}/{}/".format(
                    current_folder,
                    library_name,
                    src,
                    filename,
                    self.get_lib_folder(library_name),
                    dst
                )).execute()

                self.execute_in_folder(library_name,
                    "cd {} && patch -i {}".format(dst, filename)
                )

    def execute_in_folder(self, library_name, command):
        command = "cd {} && {}".format(self.get_lib_folder(library_name), command)
        Command(command).execute()

    def prepare(self):
        if not os.path.exists(self.fetch_folder):

            Command.executeCommands([
                RemoveDirectoryCommand(self.fetch_folder),
                CreateDirectoryCommand(self.fetch_folder),

                CreateDirectoryCommand(self.build_folder),
                CreateDirectoryCommand("{}/lib".format(self.build_folder)),
                CreateDirectoryCommand("{}/include".format(self.build_folder)),
            ])

    def common_prepare(self):
        if not os.path.exists(self.fetch_folder):
            Command.executeCommands([
                RemoveDirectoryCommand(self.fetch_folder),
                CreateDirectoryCommand(self.build_folder),

                CreateDirectoryCommand(self.build_folder),
                CreateDirectoryCommand("{}/lib".format(self.build_folder)),
                CreateDirectoryCommand("{}/include".format(self.build_folder)),
            ])

            for lib_name in config.dependencies:
                self.download(lib_name)
                self.extract(lib_name)
                self.apply_patches(lib_name)
                self.apply_injections(lib_name)

    def pop_last_dirname(self, path):
        split_path = path.split("/")
        split_path.pop()
        return "/".join(split_path)
