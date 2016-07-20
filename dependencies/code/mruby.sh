# Prepare
CODE_DIR=`dirname "${BASH_SOURCE[0]}"`
source $CODE_DIR/prepare.sh

cp -r include/* $HX3D_LINUX_INC
cp -r include/* $HX3D_ANDROID_INC

ANDROID_NDK_HOME=$ANDROID_NDK make

cp build/host/lib/libmruby.a $HX3D_LINUX_LIB
cp build/android-v/lib/libmruby.a $HX3D_ANDROID_LIB/armeabi
cp build/android-v7a/lib/libmruby.a $HX3D_ANDROID_LIB/armeabi-v7a
