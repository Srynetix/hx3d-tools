from utils.frozen_dict import FrozenDict

config = FrozenDict({
    "cxx_compiler": "g++",
    "debug_mode": True,
    "debugger": "gdb",

    "android_toolchain": "/opt/custom-ndk",
    "android_build_type": "Debug",
})
