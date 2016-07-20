# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

cp -r include/* $HX3D_LINUX_INC

mkdir -p .linuxb
cd .linuxb
  cmake -G Ninja -DYAML_CPP_BUILD_TOOLS=OFF -DBUILD_SHARED_LIBS=OFF ..
  ninja

  cp libyaml-cpp.a $HX3D_LINUX_LIB
cd ..

######################
## ANDROID

cp -r include/* $HX3D_ANDROID_INC

mkdir -p .androidb
cd .androidb
  cmake -G Ninja -DYAML_CPP_BUILD_TOOLS=OFF -DBUILD_SHARED_LIBS=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi-v7a" ..
  ninja

  cp libyaml-cpp.a $HX3D_ANDROID_LIB/armeabi-v7a/


  cmake -G Ninja -DYAML_CPP_BUILD_TOOLS=OFF -DBUILD_SHARED_LIBS=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi" ..
  ninja

  cp libyaml-cpp.a $HX3D_ANDROID_LIB/armeabi/
cd ..
