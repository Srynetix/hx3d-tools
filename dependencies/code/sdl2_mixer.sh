# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

# Preparing
mkdir -p $HX3D_LINUX_INC/SDL2

CFLAGS=-fPIC CPPFLAGS=-fPIC LDFLAGS=-fPIC ./configure --prefix=$(pwd)/.linuxb --disable-shared --disable-sdltest
make && make install

cp .linuxb/include/SDL2/SDL_mixer.h $HX3D_LINUX_INC/SDL2/
cp .linuxb/lib/libSDL2_mixer.a $HX3D_LINUX_LIB

######################
## ANDROID

mkdir -p $HX3D_ANDROID_INC/SDL2

ndk-build NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=./Android.mk NDK_APPLICATION_MK=./Application.mk
cp obj/local/armeabi/libSDL2_mixer.a $HX3D_ANDROID_LIB/armeabi
cp obj/local/armeabi-v7a/libSDL2_mixer.a $HX3D_ANDROID_LIB/armeabi-v7a
cp SDL_mixer.h $HX3D_ANDROID_INC/SDL2
