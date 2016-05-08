from hx3dtoolkit.platforms.handler import Handler
from hx3dtoolkit.commands import *
from hx3dtoolkit.config import config
from hx3dtoolkit.utils.color_print import color_print

class AndroidHandler(Handler):
    def __init__(self, command, args):
        super().__init__(command, args)

    #####

    def clean(self):
        super().clean()

        Command.executeCommands([
            RemoveDirectoryCommand("game/android/assets"),
            RemoveDirectoryCommand("game/ext/hx3d"),
            RemoveDirectoryCommand("game/jni/include"),
            RemoveDirectoryCommand("tests/android/assets"),
            RemoveDirectoryCommand("tests/android/ext/hx3d"),
            RemoveDirectoryCommand("tests/android/jni/include")
        ])

    def build(self):
        CreateDirectoryCommand(self.build_folder).execute()
        tests_active = "-DTESTS=ON" if self.tests else ""

        Command.executeCommands([

            # Engine
            Command(\
                "cd {} && \
                cmake -GNinja \
                -DANDROID_STANDALONE_TOOLCHAIN={} \
                -DCMAKE_TOOLCHAIN_FILE=cmake/dependencies/android.toolchain.cmake \
                -DANDROID_ABI=armeabi-v7a \
                -DCMAKE_BUILD_TYPE={} {} {} .."
                .format(self.build_folder, config.android_toolchain, config.android_build_type, self.get_providers_command(), tests_active)
            ),

            Command("cd {} && ninja".format(self.build_folder))
        ])

        if self.tests:
            android_path = "tests/android/ext/hx3d"
            CreateDirectoryCommand(android_path).execute()

            Command.executeCommands([
                CopyFileCommand(
                    "{}/engine/libhx3d.so".format(self.build_folder),
                    "{}/libhx3d.so".format(android_path)
                ),
                CopyFileCommand(
                    "{}/tests/libtests.so".format(self.build_folder),
                    "{}/libtests.so".format(android_path)
                ),

                CopyDirectoryCommand(
                    "engine/include/hx3d",
                    "tests/android/jni/include/hx3d"
                ),
                CopyDirectoryCommand(
                    "tests/core/include/tests",
                    "tests/android/jni/include/tests",
                ),

                CopyDirectoryCommand(
                    "engine/assets",
                    "tests/android/assets"
                ),
                CopyDirectoryCommand(
                    "tests/assets",
                    "tests/android/assets"
                ),
            ])

            color_print("> NDK Building...")
            Command("cd tests/android && ndk-build NDK-DEBUG=1").execute()

            color_print("> ANT Building...")
            Command("cd tests/android && ant debug -q").execute()

        else:
            android_path = "game/android/ext/hx3d"
            CreateDirectoryCommand(android_path).execute()

            Command.executeCommands([
                CopyFileCommand(
                    "{}/engine/libhx3d.so".format(self.build_folder),
                    "{}/libhx3d.so".format(android_path)
                ),
                CopyFileCommand(
                    "{}/game/libgame.so".format(self.build_folder),
                    "{}/libgame.so".format(android_path)
                ),

                CopyDirectoryCommand(
                    "engine/include/hx3d",
                    "game/android/jni/include/hx3d"
                ),
                CopyDirectoryCommand(
                    "game/core/include/game",
                    "game/android/jni/include/game",
                ),

                CopyDirectoryCommand(
                    "engine/assets",
                    "game/android/assets"
                ),
                CopyDirectoryCommand(
                    "game/assets",
                    "game/android/assets"
                ),
            ])

            color_print("> NDK Building...")
            Command("cd game/android && ndk-build NDK-DEBUG=1").execute()

            color_print("> ANT Building...")
            Command("cd game/android && ant debug -q").execute()

    def execute(self):
        self.check_for_build_folder()

        if self.tests:
            Command.executeCommands([
                Command("cd tests/android && ant debug install -q"),
            ])
        else:
            Command.executeCommands([
                Command("cd game/android && ant debug install -q")
            ])


    def dep_build(self):
        pass

    def package(self):
        pass
