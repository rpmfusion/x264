#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
git=$(date +%Y%m%d)
git=20100130

pushd "$tmp"
git clone git://git.videolan.org/x264.git x264-$git
pushd x264-$git
git checkout 3659b8124a809c39d61a28bdf1b235e81c02b06d
./version.sh .
find . -type d -name .git -print0 | xargs -0r rm -rf
popd
tar jcf "$pwd"/x264-$git.tar.bz2 x264-$git
popd >/dev/null
