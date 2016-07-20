# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

# Preparing
mkdir -p .linuxb
cp -r include/* $HX3D_LINUX_INC/

cd .linuxb
  cmake -G Ninja .. -DWITH_ZLIB=OFF -DWITH_HarfBuzz=OFF -DWITH_BZip2=OFF -DWITH_PNG=OFF
  ninja

  cp libfreetype.a $HX3D_LINUX_LIB/
  cp -r include/* $HX3D_LINUX_INC/
cd ..

#######################
## Android

mkdir -p .androidb

cp -r include/* $HX3D_ANDROID_INC/

cd .androidb
  unset ANDROID_NDK
  cmake -G Ninja -DWITH_ZLIB=OFF -DWITH_HarfBuzz=OFF -DWITH_BZip2=OFF -DWITH_PNG=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi-v7a" ..
  ninja

  cp libfreetype.a $HX3D_ANDROID_LIB/armeabi-v7a/
  cp -r include/* $HX3D_ANDROID_INC/

  cmake -G Ninja -DWITH_ZLIB=OFF -DWITH_HarfBuzz=OFF -DWITH_BZip2=OFF -DWITH_PNG=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi" ..
  ninja

  cp libfreetype.a $HX3D_ANDROID_LIB/armeabi/
cd ..
