# Dependency fetch

from commands import *
from config import config
from utils import color_print
from dependencies.colorama import Fore, Style
from contextlib import contextmanager
import sys
import os

def pop_last_dirname(path):
    split_path = path.split("/")
    split_path.pop()
    return "/".join(split_path)

def fetch_library_info(library):
    try:
        return next(x for x in config.dependencies if x["name"] == library)
    except StopIteration:
        color_print("  Library `` does not exist.", color=Fore.RED)
        sys.exit(1)

def get_fetch_folder(platform):
    return "_dep_fetch_{}".format(platform)

def get_build_folder(platform):
    return "{}/build".format(get_fetch_folder(platform))

def download_source(platform, library_info):
    url = library_info["url"]
    filename = library_info["filename"]

    if config.debug_mode:
        color_print("  - Downloading `{}` ({})".format(library_info["name"], filename))

    Command("cd {} && curl --progress-bar {} > {}".format(get_fetch_folder(platform), url, filename)).execute()

def extract_source(platform, library_info):
    filename = library_info["filename"]
    extension = library_info["extension"]
    folder = get_fetch_folder(platform)

    if config.debug_mode:
        color_print("  - Extracting `{}`".format(filename))

    if extension == "tar.gz":
        Command("cd {} && tar -xf {}".format(folder, filename)).execute()
    elif extension == "zip":
        Command("cd {} && unzip -q {}".format(folder, filename)).execute()
    else:
        color_print("    /!\\ Unsupported type: {}".format(extension), color=Fore.RED)
        sys.exit(1)

def get_folder_location(platform, library_info):
    return "{}/{}".format(get_fetch_folder(platform), library_info["folder"])

def execute_in_folder(platform, library_info, command):
    command = "cd {} && {}".format(get_folder_location(platform, library_info), command)
    Command(command).execute()

def multiple_executions_in_folder(platform, library_info, commands):
    for command in commands:
        execute_in_folder(platform, library_info, command)

def apply_patches(platform, library_info):
    if not "patches" in library_info:
        if config.debug_mode:
            color_print("  - No patches for {}".format(library_info["name"]))
    else:
        patches = library_info["patches"]
        for patch in patches:
            if config.debug_mode:
                color_print("  - Applying patch `{}`".format(patch["name"]))

            filename = patch["filename"]
            src = patch["src"]
            dst = patch["dst"]
            current_folder = pop_last_dirname(os.path.dirname(os.path.realpath(__file__)))

            Command("cp {}/assets/patches/{}/{}/{} {}/{}/".format(
                current_folder,
                library_info["name"],
                src,
                filename,
                get_folder_location(platform, library_info),
                dst
            )).execute()

            execute_in_folder(platform, library_info,
                "cd {} && patch -i {}".format(dst, filename)
            )

def apply_injections(platform, library_info):
    if not "injections" in library_info:
        if config.debug_mode:
            color_print("  - No injections for {}".format(library_info["name"]))
    else:
        injections = library_info["injections"]
        for injection in injections:
            if config.debug_mode:
                color_print("  - Injecting file `{}` for `{}`".format(injection["name"], library_info["name"]))

            filename = injection["filename"]
            src = injection["src"]
            dst = injection["dst"]
            current_folder = pop_last_dirname(os.path.dirname(os.path.realpath(__file__)))

            Command("cp {}/assets/patches/{}/{}/{} {}/{}/".format(
                current_folder,
                library_info["name"],
                src,
                filename,
                get_folder_location(platform, library_info),
                dst
            )).execute()

@contextmanager
def fetch_library(platform, library_name):
    try:
        library_info = fetch_library_info(library_name)
        fetch_source(platform, library_info)

        yield library_info
    finally:
        print("I Should Clean")

def fetch_source(platform, library_info):
    download_source(platform, library_info)
    extract_source(platform, library_info)
    apply_patches(platform, library_info)
    apply_injections(platform, library_info)

    color_print("> Dependency `{}` successfully fetched for {}".format(library_info["name"], platform))
