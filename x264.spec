%define snapshot 20081213
%define git 9089d21

Summary: H264/AVC video streams encoder
Name: x264
Version: 0.0.0
Release: 0.20.%{snapshot}git%{git}%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://developers.videolan.org/x264.html
Source0: http://rpm.greysector.net/livna/%{name}-%{snapshot}.tar.bz2
Source1: x264-snapshot.sh
Patch0: %{name}-rpm.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -u -n)
BuildRequires: gpac-devel
%ifarch x86_64 %{ix86}
BuildRequires: yasm
%endif
Requires: %{name}-libs = %{version}-%{release}
Obsoletes: %{name}-gui < 0.0.0-0.19

%description
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the frontend.

%package libs
Summary: Library for encoding H264/AVC video streams
Group: Development/Libraries
Obsoletes: x264 < 0.0.0-0.13.20080420

%description libs
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

%package devel
Summary: Development files for the x264 library
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
x264 is a free library for encoding H264/AVC video streams, written from
scratch.

This package contains the development files.

%define x_configure \
./configure \\\
	--host=%{_target_platform} \\\
	--prefix=%{_prefix} \\\
	--exec-prefix=%{_exec_prefix} \\\
	--bindir=%{_bindir} \\\
	--libdir=%{_libdir} \\\
	--includedir=%{_includedir} \\\
	--extra-cflags="$RPM_OPT_FLAGS" \\\
	--enable-mp4-output \\\
	%{?_with_visualize:--enable-visualize} \\\
	--enable-pthread \\\
	--enable-debug \\\
	--enable-shared \\\
	--enable-pic


%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p1 -b .r
# AUTHORS file is in iso-8859-1
iconv -f iso-8859-1 -t utf-8 -o AUTHORS.utf8 AUTHORS
mv -f AUTHORS.utf8 AUTHORS

%build
%{x_configure}

%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install

%clean
%{__rm} -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(644, root, root, 0755)
%doc AUTHORS COPYING
%attr(755,root,root) %{_bindir}/x264

%files libs
%defattr(644, root, root, 0755)
%{_libdir}/libx264.so.*

%files devel
%defattr(644, root, root, 0755)
%doc doc/ratecontrol.txt doc/vui.txt
%{_includedir}/x264.h
%{_libdir}/libx264.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sat Dec 13 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.20.20081213git9089d21
- 20081213 snapshot
- drop the libs split on x86, it doesn't work right for P3/AthlonXP
- drop obsolete patch

* Thu Dec 04 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4.1
- fix compilation on ppc

* Tue Dec 02 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.19.20081202git71d34b4
- 20081202 snapshot
- bring back asm optimized/unoptimized libs split
- rebase and improve patch
- GUI dropped upstream
- dropped redundant BRs

* Mon Nov 17 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.18.20080905
- partially revert latest changes (the separate sse2 libs part) until selinux
  policy catches up

* Fri Nov 07 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.17.20080905
- build libs without asm optimizations for less capable x86 CPUs (livna bug #2066)
- fix missing 0 in Obsoletes version (never caused any problems)

* Fri Sep 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.16.20080905
- 20080905 snapshot
- use yasm on all supported arches
- include mp4 output support via gpac by default
- drop/move obsolete fixups from %%prep
- fix icon filename in desktop file

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.0.0-0.15.20080613
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.14.20080613
- 20080613 snapshot (.so >= 59 is required by current mencoder)

* Mon May 05 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.13.20080420
- 20080420 snapshot
- split libs into a separate package
- svn -> git
- drop obsolete execstack patch
- fixed summaries and descriptions

* Wed Feb 27 2008 Dominik Mierzejewski <rpm@greysector.net> 0.0.0-0.12.20080227
- 20080227 snapshot
- fix build with gpac

* Tue Nov 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.0.0-0.11.20070819
- Merge freshrpms spec into livna spec for rpmfusion:
- Change version from 0 to 0.0.0 so that it is equal to the freshrpms versions,
  otherwise we would be older according to rpm version compare.
- Add Provides and Obsoletes x264-gtk to x264-gui for upgrade path from
  freshrpms
- Fix icon cache update scripts

* Sun Sep 30 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0-0.10.20070819
- Fix use of execstack on i386, closes livna bug #1659

* Sun Aug 19 2007 Dominik Mierzejewski <rpm@greysector.net> 0-0.9.20070819
- 20070819 snapshot, closes bug #1560

* Thu Nov 09 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.8.20061028
- use PIC on all platforms, fixes bug #1243

* Sun Oct 29 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.7.20061028
- fix desktop entry categories for devel

* Sun Oct 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.6.20061028
- fix BRs
- handle menu icon properly

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.5.20061028
- fix bad patch chunk
- fix 32bit build on x86_64

* Sat Oct 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 0-0.4.20061028
- Don't let ./configure to guess arch, pass it ourselves.
- Drop X-Livna desktop entry category.

* Sat Oct 28 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.3.20061028
- added GUI (based on kwizart's idea)
- latest snapshot
- added some docs to -devel

* Sun Oct 01 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.2.20061001
- add snapshot generator script
- fix make install
- make nasm/yasm BRs arch-dependent
- configure is not autoconf-based, call it directly

* Sat Sep 30 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.569
- Updated to latest SVN trunk
- specfile cleanups

* Mon Sep 04 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.558
- Updated to latest SVN trunk
- FE compliance

* Sun Mar 12 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.467
- Updated to latest SVN trunk
- Build shared library
- mp4 output requires gpac

* Mon Jan 02 2006 Dominik Mierzejewski <rpm@greysector.net> 0-0.1.394
- Updated to latest SVN trunk
- Change versioning scheme

* Sun Nov 27 2005 Dominik Mierzejewski <rpm@greysector.net> 0.0.375-1
- Updated to latest SVN trunk
- Added pkgconfig file to -devel

* Tue Oct  4 2005 Matthias Saou <http://freshrpms.net/> 0.0.315-1
- Update to svn 315.
- Disable vizualize since otherwise programs trying to link without -lX11 will
  fail (cinelerra in this particular case).

* Mon Aug 15 2005 Matthias Saou <http://freshrpms.net/> 0.0.285-1
- Update to svn 285.
- Add yasm build requirement (needed on x86_64).
- Replace X11 lib with lib/lib64 to fix x86_64 build.

* Tue Aug  2 2005 Matthias Saou <http://freshrpms.net/> 0.0.281-1
- Update to svn 281.

* Mon Jul 11 2005 Matthias Saou <http://freshrpms.net/> 0.0.273-1
- Initial RPM release.
