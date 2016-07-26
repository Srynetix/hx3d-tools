# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

# Preparing
mkdir -p .linuxb
cp include/yaml.h $HX3D_LINUX_INC/

cd .linuxb
  cmake -G Ninja ..
  ninja

  cp libyaml.a $HX3D_LINUX_LIB/
cd ..

#######################
## Android

mkdir -p .androidb

cp include/yaml.h $HX3D_ANDROID_INC/

cd .androidb
  unset ANDROID_NDK
  cmake -G Ninja -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi-v7a" ..
  ninja

  cp libyaml.a $HX3D_ANDROID_LIB/armeabi-v7a/

  cmake -G Ninja -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi" ..
  ninja

  cp libyaml.a $HX3D_ANDROID_LIB/armeabi/
cd ..
