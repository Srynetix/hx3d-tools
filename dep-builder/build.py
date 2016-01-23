#!/usr/bin/env python

import argparse
import os
import re

urls = {
    "SDL2": {
        "name": "SDL2",
        "url": "https://www.libsdl.org/release/SDL2-2.0.4.zip",
        "filename": "SDL2-2.0.4.zip",
        "folder": "SDL2-2.0.4",
        "extension": "zip"
    },
    "SDL2_mixer": {
        "name": "SDL2_mixer",
        "url": "https://www.libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.1.zip",
        "filename": "SDL2_mixer-2.0.1.zip",
        "folder": "SDL2_mixer-2.0.1",
        "extension": "zip",
        "patches": {
            "SDL location": {
                "filename": "project.pbxproj.patch",
                "src": "patches/SDL2_mixer",
                "dst": "Xcode-iOS/SDL_mixer.xcodeproj"
            }
        }
    },
    "freetype": {
        "name": "freetype",
        "url": "http://ftp.igh.cnrs.fr/pub/nongnu/freetype/freetype-2.6.2.tar.gz",
        "filename": "freetype-2.6.2.tar.gz",
        "folder": "freetype-2.6.2",
        "extension": "tar.gz",
        "patches": {
            "CMake Lists": {
                "filename": "CMakeLists.txt.patch",
                "src": "patches/freetype",
                "dst": "."
            },
            "iOS CMake": {
                "filename": "iOS.cmake.patch",
                "src": "patches/freetype",
                "dst": "builds/cmake"
            }
        }
    },
    "freetype-gl": {
        "name": "freetype-gl",
        "url": "https://codeload.github.com/rougier/freetype-gl/zip/master",
        "filename": "freetype-gl.zip",
        "folder": "freetype-gl-master",
        "extension": "zip",
        "patches": {
            "CMake Lists": {
                "filename": "CMakeLists.txt.patch",
                "src": "patches/freetype-gl",
                "dst": "."
            }
        },
        "injections": {
            "iOS CMake": {
                "filename": "iOS.cmake",
                "src": "patches/freetype-gl",
                "dst": "CMakeModules"
            }
        }
    }
}

def execCommand(command):
    code = os.system(command)
    if code != 0:
        print("/!> Error.")
        exit(code)

def executeInFolder(key, command):
    execCommand("cd src/{} && {}".format(urls[key]["folder"], command))

def extract(key):
    filename = urls[key]["filename"]
    extension = urls[key]["extension"]

    print("Extracting {}".format(filename))
    if extension == "tar.gz":
        execCommand("cd src && tar -xf {}".format(filename))
    elif extension == "zip":
        execCommand("cd src && unzip -q {}".format(filename))
    else:
        print("Unsupported type: {}".format(ext))

def getFolderLocation(key):
    return "src/{}".format(urls[key]["folder"])

def clean(key):
    filename = urls[key]["filename"]
    print("Cleaning {}".format(key))
    execCommand("cd src && rm {} 2> /dev/null".format(filename))

def download(key):
    url = urls[key]["url"]
    filename = urls[key]["filename"]

    print("Downloading {} ({})".format(key, filename))
    execCommand("cd src && curl --progress-bar {} > {}".format(url, filename))

def fetchSource():
    execCommand("mkdir -p src")

    for lib in urls:
        download(lib)
        extract(lib)
        executePatches(lib)
        executeInjections(lib)
        # clean(lib)

    print("Fetching includes...")
    fetchIncludes()

def executeInjections(key):
    if not "injections" in urls[key]:
        print("No injections for " + key)
        return

    injections = urls[key]["injections"]
    for injection in injections:
        print("Adding injection for {} ({})".format(key, injection))
        filename = urls[key]["injections"][injection]["filename"]
        src = urls[key]["injections"][injection]["src"]
        dst = urls[key]["injections"][injection]["dst"]

        execCommand("cp {}/{} {}/{}/".format(src, filename, getFolderLocation(key), dst))

def executePatches(key):
    if not "patches" in urls[key]:
        print("No patches for " + key)
        return

    patches = urls[key]["patches"]
    for patch in patches:
        print("Applying patch for {} ({})".format(key, patch))
        filename = urls[key]["patches"][patch]["filename"]
        src = urls[key]["patches"][patch]["src"]
        dst = urls[key]["patches"][patch]["dst"]

        execCommand("cp {}/{} {}/{}/".format(src, filename, getFolderLocation(key), dst))
        executeInFolder(key, "cd {} && patch -i {}".format(dst, filename))


def fetchIncludes():
    execCommand("mkdir -p build/include")

    # SDL2
    execCommand("mkdir -p build/include/SDL2")
    executeInFolder("SDL2", "cp -r include/*.h ../../build/include/SDL2/")

    # SDL2_mixer
    executeInFolder("SDL2_mixer", "cp SDL_mixer.h ../../build/include/SDL2/")

    # freetype
    execCommand("mkdir -p build/include/freetype2")
    executeInFolder("freetype", "cp -r include/freetype/* ../../build/include/freetype2/")
    executeInFolder("freetype", "cp include/ft2build.h ../../build/include/freetype2/")

    # freetype-gl
    execCommand("mkdir -p build/include/freetype-gl")
    executeInFolder("freetype-gl", "cp *.h ../../build/include/freetype-gl/")

def buildIOS():
    execCommand("mkdir -p build/lib/ios")

    # SDL2
    executeInFolder("SDL2", "cd Xcode-iOS/SDL && xcodebuild -target libSDL -configuration Release")
    executeInFolder("SDL2", "cp Xcode-iOS/SDL/build/Release-iphoneos/libSDL2.a ../../build/lib/ios")

    # SDL2_mixer
    executeInFolder("SDL2_mixer", "cd Xcode-iOS && xcodebuild -configuration Release")
    executeInFolder("SDL2_mixer", "cp Xcode-iOS/build/Release-iphoneos/libSDL2_mixer.a ../../build/lib/ios")

    # freetype
    executeInFolder("freetype", "mkdir -p ios-build")
    executeInFolder("freetype", "cd ios-build && cmake -G Xcode -D IOS_PLATFORM=OS ..")
    executeInFolder("freetype", "cd ios-build && xcodebuild -configuration Release -target ALL_BUILD")
    executeInFolder("freetype", "cp ios-build/Release-iphoneos/libfreetype.a ../../build/lib/ios")

    # freetype-gl
    executeInFolder("freetype-gl", "mkdir -p ios-build")
    executeInFolder("freetype-gl", "cd ios-build && cmake -DCMAKE_TOOLCHAIN_FILE=CMakeModules/iOS.cmake -G Xcode -DIOS_PLATFORM=OS -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd ios-build && xcodebuild -configuration Release -target freetype-gl")
    executeInFolder("freetype-gl", "cp ios-build/Release-iphoneos/libfreetype-gl.a ../../build/lib/ios")


def buildIOSSim():
    execCommand("mkdir -p build/lib/ios-sim")

    # SDL2
    executeInFolder("SDL2", "cd Xcode-iOS/SDL && xcodebuild -target libSDL -configuration Release -sdk iphonesimulator")
    executeInFolder("SDL2", "cp Xcode-iOS/SDL/build/Release-iphonesimulator/libSDL2.a ../../build/lib/ios-sim")

    # SDL2_mixer
    executeInFolder("SDL2_mixer", "cd Xcode-iOS && xcodebuild -configuration Release -sdk iphonesimulator")
    executeInFolder("SDL2_mixer", "cp Xcode-iOS/build/Release-iphonesimulator/libSDL2_mixer.a ../../build/lib/ios-sim")

    # freetype
    executeInFolder("freetype", "mkdir -p ios-sim-build")
    executeInFolder("freetype", "cd ios-sim-build && cmake -G Xcode -D IOS_PLATFORM=SIMULATOR ..")
    executeInFolder("freetype", "cd ios-sim-build && xcodebuild -configuration Release -target ALL_BUILD")
    executeInFolder("freetype", "cp ios-sim-build/Release-iphonesimulator/libfreetype.a ../../build/lib/ios-sim")

    # freetype-gl
    executeInFolder("freetype-gl", "mkdir -p ios-sim-build")
    executeInFolder("freetype-gl", "cd ios-sim-build && cmake -DCMAKE_TOOLCHAIN_FILE=CMakeModules/iOS.cmake -G Xcode -DIOS_PLATFORM=SIMULATOR -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd ios-sim-build && xcodebuild -configuration Release -target freetype-gl")
    executeInFolder("freetype-gl", "cp ios-sim-build/Release-iphonesimulator/libfreetype-gl.a ../../build/lib/ios-sim")


def main():
    available_systems = ["ios, ios-sim"]

    print()
    print("** Dependencies builder **")
    print()

    print("Before choosing a system, fetch the content:")
    print("\t~> ./build.py fetch")
    print()

    print("To remove the sources:")
    print("\t~> ./build.py clean")
    print()

    parser = argparse.ArgumentParser(description="Build the dependencies")
    parser.add_argument("system", help="System/Fetch")
    args = parser.parse_args()

    if args.system == "fetch":
        fetchSource()
    elif args.system == "clean":
        print("Cleaning...")
        execCommand("rm -r src")
    elif args.system == "ios":
        print("Building for iOS")
        buildIOS()
    elif args.system == "ios-sim":
        print("Building for iOS Simulator")
        buildIOSSim()
    else:
        print("Unsupported. Available systems: ", available_systems)

if __name__ == "__main__":
    main()
