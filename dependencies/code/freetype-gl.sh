# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

######################
## LINUX

mkdir -p $HX3D_LINUX_INC/freetype-gl
cp *.h $HX3D_LINUX_INC/freetype-gl

mkdir -p .linuxb
cd .linuxb
  cmake -G Ninja .. -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -DFREETYPE_INCLUDE_DIR="$HX3D_LINUX_INC"
  ninja

  cp libfreetype-gl.a $HX3D_LINUX_LIB
cd ..

#######################
## ANDROID

mkdir -p $HX3D_ANDROID_INC/freetype-gl
cp *.h $HX3D_ANDROID_INC/freetype-gl

mkdir -p .androidb
cd .androidb
  cmake -G Ninja -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi-v7a" -DFREETYPE_INCLUDE_DIR="$HX3D_LINUX_INC" ..
  ninja

  cp libfreetype-gl.a $HX3D_ANDROID_LIB/armeabi-v7a/

  cmake -G Ninja -Dfreetype-gl_BUILD_DEMOS=OFF -Dfreetype-gl_BUILD_APIDOC=OFF -Dfreetype-gl_BUILD_MAKEFONT=OFF -DANDROID_STANDALONE_TOOLCHAIN=$ANDROID_TC -DCMAKE_TOOLCHAIN_FILE=$CMAKE_TOOLCHAIN_FILE -DANDROID_ABI="armeabi" -DFREETYPE_INCLUDE_DIR="$HX3D_LINUX_INC" ..
  ninja

  cp libfreetype-gl.a $HX3D_ANDROID_LIB/armeabi/
cd ..
