from colorama import Fore, Style

from hx3dtoolkit.config import config
from hx3dtoolkit.utils.dependency_fetch import pop_last_dirname
from hx3dtoolkit.utils.color_print import color_print as cprint
from hx3dtoolkit.commands import *

import shutil
import re
import os

def _explore_directory(directory):
    file_list = []
    folder_list = []

    for root, directories, files in os.walk(directory):
        for d in directories:
            filepath = os.path.join(root, d)
            folder_list.append(filepath)
        for filename in files:
            filepath = os.path.join(root, filename)
            file_list.append(filepath)

    return folder_list, file_list

def _replace_content(content, params):
    new_content = content
    for key, value in params.items():
        occurences = re.findall(r"\<\#\[({})\]\#\>".format(key), new_content)
        if len(occurences) > 0:
            new_content = re.sub(r"\<\#\[({})\]\#\>".format(key), value, new_content)

    # Last check
    occurences = re.findall(r"\<\#\[(\w+)\]\#\>", new_content)
    if len(occurences) > 0:
        print()
        cprint("> /!\\ Error: variables remains.", Fore.RED)
        for oc in occurences:
            cprint("\t- Variable: {}".format(oc), Fore.RED)
        print()

    return new_content

# GENERATE PACKAGE PATH ####################################

def _package_path(name):
    path = re.sub(r'\.', '/', name)
    return path

# GENERATE PROJECT FROM TEMPLATE ###########################

def _generate_template(params):
    cprint("> Building new game `{}` in the folder `{}`.".format(params["game_name"], params["folder"]), color=Fore.GREEN)

    # Template list
    tool_directory = pop_last_dirname(os.path.dirname(os.path.realpath(__file__)))
    folders, files = _explore_directory("{}/assets/template/".format(tool_directory))
    new_folders = []
    new_files = []

    for f in files:
        new_file_name = _replace_content(f, params)
        new_files.append(new_file_name.replace("{}/assets/template/".format(tool_directory), params["folder"]))

    for d in folders:
        new_dir_name = _replace_content(d, params)
        new_folders.append(new_dir_name.replace("{}/assets/template/".format(tool_directory), params["folder"]))

    # Folders copy
    print()
    cprint("> Creating folder structure", color=Fore.GREEN)
    for i in range(len(new_folders)):
        old = folders[i]
        new = new_folders[i]

        if not os.path.exists(new):
            os.makedirs(new)

    # Files copy
    print()
    cprint("> Copying and templating files", color=Fore.GREEN)
    for i in range(len(new_files)):
        old = files[i]
        new = new_files[i]

        # File replacement
        if not new.endswith(".png") and not new.endswith(".icns"):
            old_file = open(old, "r")
            old_file_content = old_file.read()

            with open(new, "w+") as new_file:
                print("{}".format(_replace_content(old_file_content, params)), file=new_file)
        else:
            shutil.copy(old, new)

# GET THE ENGINE #########################

def _create_project(args, params):

    folder = params["folder"]

    # Folder creation
    if not os.path.exists(folder):
        os.makedirs(folder)

    if not args.game_only:

        # Framework check
        cprint("> Fetching the hx3d framework to `{}`.".format(folder), color=Fore.GREEN)

        Command.executeCommands([
            Command("git clone --depth=1 {} -b {} {}".format(config.generator.framework.repository, config.generator.framework.branch, folder)),
            Command("cd {} && ./clone_dependencies.sh".format(folder)),
            Command("cd {} && git clone --depth=1 {} -b {} tools".format(folder, config.generator.tools.repository, config.generator.tools.branch)),
            Command("cd {} && rm -rf .git".format(folder))
        ])

    # Generate template
    _generate_template(params)

def generate(args):

    params = {
        "game_name": args.name[0],
        "game_name_lower": args.name[0].lower(),
        "game_name_upper": args.name[0].upper(),
        "folder": args.directory[0] + "/",
        "android_package_name": args.package_name[0],
        "android_package_path": _package_path(args.package_name[0]),
        "android_sdk_dir": "/opt/android-sdk"
    }

    _create_project(args, params)
