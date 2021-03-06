from hx3dtoolkit.platforms.handler import Handler
from hx3dtoolkit.platforms.common_handler import CommonHandler
from hx3dtoolkit.commands import *
from hx3dtoolkit.config import config
from hx3dtoolkit.utils.dependency_fetch import DepFetcher
import os

class LinuxHandler(Handler):
    def __init__(self, command, args):
        super().__init__(command, args)
        self.dep_fetcher = DepFetcher(self)

    #####

    def build(self):
        tests_active = "-DTESTS=ON" if self.tests else "-DGAME=ON"
        game_dir = "tests" if self.tests else "game"

        Command.executeCommands([
            CreateDirectoryCommand(self.build_folder),
            Command("cd _build_linux && CXX={} cmake -G Ninja {} {} ..".format(config.cxx_compiler, self.get_providers_command(), tests_active)),
            Command("cd _build_linux && ninja", stdout=True),
            CopyDirectoryCommand("engine/assets", "_build_linux/{}/assets".format(game_dir)),
            CopyDirectoryCommand("{}/assets".format(game_dir), "_build_linux/{}/assets".format(game_dir)),
        ])

    def execute(self):
        self.check_for_build_folder()

        game_dir = "tests" if self.tests else "game"
        debug_cmd = config.debugger if self.debug else ""
        memcheck_cmd = config.memcheck.tool if self.memcheck else ""

        Command.executeCommands([
            Command("cd _build_linux/{dir} && {cmd} ./{dir}".format(cmd=debug_cmd or memcheck_cmd, dir=game_dir), stdout=True),
        ])

    def dep_fetch(self):
        
        # Build
        self.dep_fetcher.execute_commands("SDL2", [
            "mkdir -p ../build/include/SDL2",
            "mkdir -p linux-build",
            "cd linux-build && cmake -G Ninja -D SDL_SHARED=OFF ..",
            "cd linux-build && ninja",
            "cp -r linux-build/include/* ../build/include/SDL2/",
            "cp -r linux-build/*.a ../build/lib/",
        ])

        # if not os.path.exists(get_fetch_folder("common")):
        #     MainHandler(self.command, self.args).handle()
        #
        # super().dep_fetch()
        #
        # with fetch_library(self.platform, "SDL2", source=not args.use_cache) as library_info:
        #     multiple_executions_in_folder(self.platform, library_info, [
        #         "mkdir -p ../build/include/SDL2",
        #         "mkdir -p linux-build",
        #         "cd linux-build && cmake -G Ninja -D SDL_SHARED=OFF ..",
        #         "cd linux-build && ninja",
        #         "cp -r linux-build/include/* ../build/include/SDL2/",
        #         "cp -r linux-build/*.a ../build/lib/",
        #     ])
        #
        # with fetch_library(self.platform, "SDL2_mixer", source=not args.use_cache) as library_info:
        #     multiple_executions_in_folder(self.platform, library_info, [
        #         "./configure",
        #         "make",
        #         "cp build/.libs/*.a ../build/lib/",
        #         "cp SDL_mixer.h ../build/include/SDL2/",
        #     ])
        #
        # with fetch_library(self.platform, "freetype", source=not args.use_cache) as library_info:
        #     multiple_executions_in_folder(self.platform, library_info, [
        #         "mkdir -p linux-build",
        #         "cd linux-build && cmake -G Ninja ..",
        #         "cd linux-build && ninja",
        #         "cp linux-build/*.a ../build/lib/",
        #         "cp -r linux-build/include/* ../build/include/",
        #     ])
        #
        # with fetch_library(self.platform, "freetype-gl", source=not args.use_cache) as freetype_gl:
        #     multiple_executions_in_folder(self.platform, freetype_gl, [
        #         "mkdir -p linux-build",
        #         "cd linux-build && cmake -G Ninja -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..",
        #         "cd linux-build && ninja",
        #         "cp linux-build/*.a ../build/lib/",
        #     ])
        #
        # with fetch_library(self.platform, "gtest", source=not args.use_cache) as gtest:
        #     multiple_executions_in_folder(self.platform, gtest, [
        #         "mkdir -p linux-build",
        #         "cd linux-build && cmake -G Ninja ..",
        #         "cd linux-build && ninja",
        #         "cp linux-build/libgtest.a ../build/lib/",
        #     ])

    def package(self):
        pass
