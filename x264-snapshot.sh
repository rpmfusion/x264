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

pushd "$tmp"
git clone git://git.videolan.org/x264.git x264-$git
pushd x264-$git
./version.sh .
find . -type d -name .git -print0 | xargs -0r rm -rf
popd
tar jcf "$pwd"/x264-$git.tar.bz2 x264-$git
popd >/dev/null
