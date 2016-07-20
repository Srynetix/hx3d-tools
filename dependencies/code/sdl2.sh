# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

# Preparing
mkdir -p .linuxb
mkdir -p $HX3D_LINUX_INC/SDL2
cp include/*.h $HX3D_LINUX_INC/SDL2

cd .linuxb
  # Building
  cmake -G Ninja .. -DVIDEO_WAYLAND=OFF -DSDL_SHARED=OFF
  ninja

  # Copying includes
  cp include/SDL_config.h $HX3D_LINUX_INC/SDL2
  cp libSDL2.a $HX3D_LINUX_LIB
cd ..

######################
## ANDROID

mkdir -p $HX3D_ANDROID_INC/SDL2

# Building
ndk-build NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=./Android.mk NDK_APPLICATION_MK=./Application.mk

# Copying
cp include/*.h $HX3D_ANDROID_INC/SDL2
cp libs/armeabi/libSDL2.a $HX3D_ANDROID_LIB/armeabi
cp libs/armeabi-v7a/libSDL2.a $HX3D_ANDROID_LIB/armeabi-v7a
