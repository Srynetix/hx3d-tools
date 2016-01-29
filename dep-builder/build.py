#!/usr/bin/env python

import argparse
import os
import re
import yaml

config_file = open("config.yml", "r")
content = config_file.read()

urls = yaml.load(content)
config_file.close()

def execCommand(command, error=True):
    code = os.system(command)
    if error and code != 0:
        print("/!> Error.")
        exit(code)

def executeInFolder(key, command, error=True):
    execCommand("cd src/{} && {}".format(urls[key]["folder"], command), error)

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

    # print("Fetching includes...")
    # fetchIncludes()

def executeInjections(key):
    if not "injections" in urls[key]:
        print("No injections for " + key)
        return

    injections = urls[key]["injections"]
    for injection in injections:
        print("Adding injection for {} ({})".format(key, injection["name"]))
        filename = injection["filename"]
        src = injection["src"]
        dst = injection["dst"]

        execCommand("cp patches/{}/{}/{} {}/{}/".format(key, src, filename, getFolderLocation(key), dst))

def executePatches(key):
    if not "patches" in urls[key]:
        print("No patches for " + key)
        return

    patches = urls[key]["patches"]
    for patch in patches:
        print("Applying patch for {} ({})".format(key, patch["name"]))
        filename = patch["filename"]
        src = patch["src"]
        dst = patch["dst"]

        execCommand("cp patches/{}/{}/{} {}/{}/".format(key, src, filename, getFolderLocation(key), dst))
        executeInFolder(key, "cd {} && patch -i {}".format(dst, filename))

###########################
###########################
###########################

def buildLinux():
    execCommand("mkdir -p build/linux/lib")
    execCommand("mkdir -p build/linux/include")

    # SDL2
    execCommand("mkdir -p build/linux/include/SDL2")
    executeInFolder("SDL2", "cp include/*.h ../../build/linux/include/SDL2/")
    executeInFolder("SDL2", "mkdir -p linux-build")
    executeInFolder("SDL2", "cd linux-build && cmake -G Ninja -D SDL_SHARED=OFF ..")
    executeInFolder("SDL2", "cd linux-build && ninja")
    executeInFolder("SDL2", "cp -r linux-build/include/* ../../build/linux/include/SDL2/")
    executeInFolder("SDL2", "cp linux-build/*.a ../../build/linux/lib/")

    # SDL2_mixer
    executeInFolder("SDL2_mixer", "./configure")
    executeInFolder("SDL2_mixer", "make")
    executeInFolder("SDL2_mixer", "cp build/.libs/*.a ../../build/linux/lib/")
    executeInFolder("SDL2_mixer", "cp SDL_mixer.h ../../build/linux/include/SDL2/")

    # freetype
    executeInFolder("freetype", "mkdir -p linux-build")
    executeInFolder("freetype", "cd linux-build && cmake -G Ninja -DWITH_BZip2=OFF -DWITH_HarfBuzz=OFF -DWITH_PNG=OFF -DWITH_ZLIB=OFF ..")
    executeInFolder("freetype", "cd linux-build && ninja")
    executeInFolder("freetype", "cp linux-build/*.a ../../build/linux/lib/")
    executeInFolder("freetype", "cp -r include/* ../../build/linux/include/")
    executeInFolder("freetype", "cp -r linux-build/include/* ../../build/linux/include/")

    # freetype-gl
    execCommand("mkdir -p build/linux/include/freetype-gl")
    executeInFolder("freetype-gl", "mkdir -p linux-build")
    executeInFolder("freetype-gl", "cd linux-build && cmake -G Ninja -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd linux-build && ninja")
    executeInFolder("freetype-gl", "cp linux-build/*.a ../../build/linux/lib/")
    executeInFolder("freetype-gl", "cp *.h ../../build/linux/include/freetype-gl")

    # gtest
    executeInFolder("gtest", "mkdir -p linux-build")
    executeInFolder("gtest", "cd linux-build && cmake -G Ninja -D gtest_disable_pthreads=ON ..")
    executeInFolder("gtest", "cd linux-build && ninja")
    executeInFolder("gtest", "cp linux-build/libgtest.a ../../build/linux/lib/")
    executeInFolder("gtest", "cp -r include/* ../../build/linux/include/")

def buildAndroid():
    execCommand("mkdir -p build/android/lib")
    execCommand("mkdir -p build/android/lib/armeabi")
    execCommand("mkdir -p build/android/lib/armeabi-v7a")
    execCommand("mkdir -p build/android/lib/x86")
    execCommand("mkdir -p build/android/include")

    execCommand("mkdir -p build/android/src/java/org/libsdl/app")
    execCommand("mkdir -p build/android/src/jni")

    # SDL2
    execCommand("mkdir -p build/android/include/SDL2")

    executeInFolder("SDL2", "cd build-scripts && ./androidbuild.sh org.libsdl.testgles ../test/testgles.c", False)
    executeInFolder("SDL2", "cp -r include/*.h ../../build/android/include/SDL2/")
    executeInFolder("SDL2", "cp -r build/org.libsdl.testgles/libs/armeabi/libSDL2.so ../../build/android/lib/armeabi/")
    executeInFolder("SDL2", "cp -r build/org.libsdl.testgles/libs/armeabi-v7a/libSDL2.so ../../build/android/lib/armeabi-v7a/")
    executeInFolder("SDL2", "cp -r build/org.libsdl.testgles/libs/x86/libSDL2.so ../../build/android/lib/x86/")
    executeInFolder("SDL2", "cp -r build/org.libsdl.testgles/src/org/libsdl/app/SDLActivity.java ../../build/android/src/java/org/libsdl/app/")
    executeInFolder("SDL2", "cp -r src/main/android/SDL_android_main.c ../../build/android/src/jni/")

    # SDL2_mixer
    executeInFolder("SDL2_mixer", "mkdir -p ../jni")
    executeInFolder("SDL2_mixer", "cp -r * ../jni/")
    executeInFolder("SDL2_mixer", "mv ../jni jni")
    executeInFolder("SDL2_mixer", "ndk-build")
    executeInFolder("SDL2_mixer", "cp obj/local/armeabi/libSDL2_mixer.a ../../build/android/lib/armeabi/")
    executeInFolder("SDL2_mixer", "cp obj/local/armeabi-v7a/libSDL2_mixer.a ../../build/android/lib/armeabi-v7a/")
    executeInFolder("SDL2_mixer", "cp obj/local/x86/libSDL2_mixer.a ../../build/android/lib/x86/")
    executeInFolder("SDL2_mixer", "cp SDL_mixer.h ../../build/android/include/SDL2/")
    executeInFolder("SDL2_mixer", "rm -r jni")
    
    # freetype
    executeInFolder("freetype", "mkdir -p android-build")

    executeInFolder("freetype", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=builds/cmake/android.toolchain.cmake -D ANDROID_ABI=armeabi -DWITH_BZip2=OFF -DWITH_HarfBuzz=OFF -DWITH_PNG=OFF -DWITH_ZLIB=OFF ..")
    executeInFolder("freetype", "cd android-build && ninja")
    executeInFolder("freetype", "cp android-build/libfreetype.a ../../build/android/lib/armeabi")

    executeInFolder("freetype", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=builds/cmake/android.toolchain.cmake -D ANDROID_ABI=armeabi-v7a -DWITH_BZip2=OFF -DWITH_HarfBuzz=OFF -DWITH_PNG=OFF -DWITH_ZLIB=OFF ..")
    executeInFolder("freetype", "cd android-build && ninja")
    executeInFolder("freetype", "cp android-build/libfreetype.a ../../build/android/lib/armeabi-v7a")

    executeInFolder("freetype", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=builds/cmake/android.toolchain.cmake -D ANDROID_ABI=x86 -DWITH_BZip2=OFF -DWITH_HarfBuzz=OFF -DWITH_PNG=OFF -DWITH_ZLIB=OFF ..")
    executeInFolder("freetype", "cd android-build && ninja")
    executeInFolder("freetype", "cp android-build/libfreetype.a ../../build/android/lib/x86")

    executeInFolder("freetype", "cp -r include/* ../../build/android/include/")
    executeInFolder("freetype", "cp -r android-build/include/* ../../build/android/include/")

    # freetype-gl
    execCommand("mkdir -p build/android/include/freetype-gl")
    executeInFolder("freetype-gl", "mkdir -p android-build")

    executeInFolder("freetype-gl", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=CMakeModules/android.toolchain.cmake -D ANDROID_ABI=armeabi -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd android-build && ninja")
    executeInFolder("freetype-gl", "cp android-build/libfreetype-gl.a ../../build/android/lib/armeabi")

    executeInFolder("freetype-gl", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=CMakeModules/android.toolchain.cmake -D ANDROID_ABI=armeabi-v7a -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd android-build && ninja")
    executeInFolder("freetype-gl", "cp android-build/libfreetype-gl.a ../../build/android/lib/armeabi-v7a")

    executeInFolder("freetype-gl", "cd android-build && cmake -G Ninja -D CMAKE_TOOLCHAIN_FILE=CMakeModules/android.toolchain.cmake -D ANDROID_ABI=x86 -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -Dfreetype-gl_LIBS_SUPPLIED=ON -Dfreetype-gl_GLFW_SUPPLIED=ON ..")
    executeInFolder("freetype-gl", "cd android-build && ninja")
    executeInFolder("freetype-gl", "cp android-build/libfreetype-gl.a ../../build/android/lib/x86")

    executeInFolder("freetype-gl", "cp *.h ../../build/android/include/freetype-gl")

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
    available_systems = ["ios", "ios-sim", "linux", "android"]

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
    elif args.system == "linux":
        print("Building for Linux")
        buildLinux()
    elif args.system == "ios-sim":
        print("Building for iOS Simulator")
        buildIOSSim()
    elif args.system == "android":
        print("Building for Android")
        buildAndroid()
    else:
        print("Unsupported. Available systems: ", available_systems)

if __name__ == "__main__":
    main()
