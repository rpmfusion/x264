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
date=20110620
package=x264
branch=stable
commit=2809cb6ce63817a58c5639642fe05bc50747e126

pushd "$tmp"
git clone git://git.videolan.org/${package}.git -b ${branch}
cd ${package}
git checkout ${commit}
git checkout -b rpmfusion
./version.sh > version.h
git add version.h
git commit -m "generated version.h" version.h
git archive --prefix="${package}-${branch}-${date}/" --format=tar rpmfusion | bzip2 > "$pwd"/${package}-${branch}-${date}.tar.bz2
popd >/dev/null
