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
date=$(date +%Y%m%d)
package=x264
branch=stable

pushd "$tmp"
git clone git://git.videolan.org/${package}.git -b ${branch}
cd ${package}
./version.sh > version.h
git add version.h
git commit version.h
git archive --prefix="${package}-${branch}-${date}/" --format=tar ${branch} | bzip2 > "$pwd"/${package}-${branch}-${date}.tar.bz2
popd >/dev/null
