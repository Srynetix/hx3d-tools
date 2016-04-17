from .handler import Handler
from commands import *
from config import config
from utils.dependency_fetch import get_fetch_folder, multiple_executions_in_folder, fetch_library

class MainHandler(Handler):
    def __init__(self, command, args):
        super().__init__(command, args)

    ########

    def doc(self):
        show_doc = self.args.show
        Command("doxygen").execute()

        if show_doc:
            Command("{} site/doc/html/index.html".format(config.web_browser)).execute()

    def clean(self):
        Command("rm -rf _build*", stderr=True).execute()

    def dep_fetch(self):
        fetch_folder = get_fetch_folder("common")
        build_folder = "{}/build".format(fetch_folder)

        Command.executeCommands([
            RemoveDirectoryCommand(fetch_folder),
            CreateDirectoryCommand(fetch_folder),

            CreateDirectoryCommand(build_folder),
            CreateDirectoryCommand("{}/lib".format(build_folder)),
            CreateDirectoryCommand("{}/include".format(build_folder)),
        ])

        # Common dep-fetch
        with fetch_library("common", "SDL2", source=True) as sdl2:
            multiple_executions_in_folder("common", sdl2, [
                "mkdir -p ../build/include/SDL2",
                "cp include/*.h ../build/include/SDL2/",
            ])

        with fetch_library("common", "SDL2_mixer", source=True) as sdl2mixer:
            pass

        with fetch_library("common", "freetype", source=True) as ft:
            multiple_executions_in_folder("common", ft, [
                "cp -r include/* ../build/include/",
            ])

        with fetch_library("common", "freetype-gl", source=True) as freetype_gl:
            multiple_executions_in_folder("common", freetype_gl, [
                "mkdir -p ../build/include/freetype-gl",
                "cp *.h ../build/include/freetype-gl",
            ])

        with fetch_library("common", "gtest", source=True) as gtest:
            multiple_executions_in_folder("common", gtest, [
                "cp -r include/* ../build/include/",
            ])