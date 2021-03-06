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
package=x264
branch=stable
commit=HEAD

pushd "$tmp"
git clone https://code.videolan.org/videolan/x264.git -b ${branch}

cd ${package}
tag=$(git rev-list HEAD -n 1 | cut -c 1-7)
git checkout ${commit}
git checkout -b rpmfusion
./version.sh > version.h
API="$(grep '#define X264_BUILD' < x264.h | sed 's/^.* \([1-9][0-9]*\).*$/\1/')"
date=$(git log -1 --format=%cd --date=short | tr -d \-)
git add version.h
git commit -m "generated version.h" version.h
git archive --prefix="${package}-0.$API-${date}git${tag}/" --format=tar rpmfusion | bzip2 > "$pwd"/${package}-0.$API-${date}git${tag}.tar.bz2
popd >/dev/null

echo \# globals for x264-0.$API-${date}git${tag}.tar.bz2
echo %global api $API
echo %global gitdate ${date}
echo %global gitversion ${tag}
echo
echo rpmdev-bumpspec -c \"Update to x264-0.$API-${date}git${tag} \(stable branch\)\" x264.spec
echo rfpkg scratch-build --srpm --arches x86_64
echo rfpkg new-sources x264-0.$API-${date}git${tag}.tar.bz2
echo rfpkg ci -c

