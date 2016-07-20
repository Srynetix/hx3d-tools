PREP_CODE_DIR=`dirname "${BASH_SOURCE[0]}"`

# Prepare
if [ -z $HX3D_DEP_BUILD ]; then
  echo "You need to set HX3D_DEP_BUILD to your build folder"
  exit 1
fi

HX3D_LINUX_INC=$HX3D_DEP_BUILD/linux/include
HX3D_LINUX_LIB=$HX3D_DEP_BUILD/linux/lib
HX3D_ANDROID_INC=$HX3D_DEP_BUILD/android/include
HX3D_ANDROID_LIB=$HX3D_DEP_BUILD/android/lib

mkdir -p $HX3D_LINUX_INC
mkdir -p $HX3D_LINUX_LIB
mkdir -p $HX3D_ANDROID_INC
mkdir -p $HX3D_ANDROID_LIB/armeabi
mkdir -p $HX3D_ANDROID_LIB/armeabi-v7a

## Android

ANDROID_TC=/opt/custom-ndk
CMAKE_TOOLCHAIN_FILE=$PREP_CODE_DIR/../source/utils/android.toolchain.cmake
