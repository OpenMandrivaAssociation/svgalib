%define	name	svgalib
%define	version	1.9.25
%define	major	1
%define	libname	%mklibname %{name} %{major}

Summary:	A low-level fullscreen SVGA graphics library
Name:		%{name}
Version:	%{version}
Release:	%mkrel 6
License:	Public Domain
Group:		System/Libraries
URL:		http://www.svgalib.org/
Source0:	http://www.arava.co.il/matan/svgalib/%{name}-%{version}.tar.gz
Patch0:		svgalib-1.9.21-makefiles.patch
Patch1:		svgalib-1.4.3-fhs.patch
Patch2:		svgalib-1.9.21-demos.patch
Patch3:		svgalib-1.9.21-cfg.patch
Patch4:		svgalib-1.9.25-kernel-2.6.26.patch
Patch5:		svgalib-1.9.25-LDFLAGS.diff
Patch6:		svgalib-1.9.25-round_gtf_gtfcalc_c.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} x86_64

%description
The svgalib package provides the SVGAlib low-level graphics library for
Linux. SVGAlib is a library which allows applications to use full screen
graphics on a variety of hardware platforms. Many games and utilities use
SVGAlib for their graphics.

You'll need to have the svgalib package installed if you use any of the
programs which rely on SVGAlib for their graphics support.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{libname}-devel
Summary:	Development tools for programs using the SVGAlib graphics library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
The svgalib-devel package contains the libraries and header files needed
to build programs which will use the SVGAlib low-level graphics library.

Install the svgalib-devel package if you want to develop applications
which will use the SVGAlib library. Please take note that SVGAlib is
independent from X Window System. Thus, this package is useless if you
want to develop X11 applications.

%prep

%setup -q
%patch0 -p1 -b .makefiles
%patch1 -p1 -b .fhs
%patch2 -p1 -b .demos
%patch3 -p1 -b .defaultcfg
%patch4 -p1 -b .kernel-2.6.26
%patch5 -p1 -b .LDFLAGS
%patch6 -p1 -b .round

#the testlinear demo needs svgalib's internal libvga header, so copy it to the
#demo dir
cp src/libvga.h demos

%build

make OPTIMIZE="%{optflags} -Wno-pointer-sign" \
    LDFLAGS="%{ldflags}" \
    prefix=%{_prefix} \
    NO_HELPER=y \
    INCLUDE_ET4000_DRIVER=y \
    INCLUDE_OAK_DRIVER=y \
    INCLUDE_MACH32_DRIVER=y \
    INCLUDE_ET3000_DRIVER=y \
    INCLUDE_GVGA6400_DRIVER=y \
    INCLUDE_ATI_DRIVER=y \
    INCLUDE_G450C2_DRIVER=y \
    INCLUDE_ET4000_DRIVER_TEST=y \
    INCLUDE_FBDEV_DRIVER_TEST=y \
    INCLUDE_VESA_DRIVER_TEST=y \
    shared

pushd utils
    make OPTIMIZE="%{optflags} -Wno-pointer-sign" \
    LDFLAGS="%{ldflags}" \
    prefix=%{_prefix}
popd

pushd threeDKit
make OPTIMIZE="%{optflags} -Wno-pointer-sign -I../gl" \
    LDFLAGS="%{ldflags}" \
    LIBS="-L../sharedlib -lm -lvgagl -lvga" \
    prefix=%{_prefix} lib3dkit.so.%{version}
popd

%ifarch %{ix86}
pushd lrmi-0.9
    make CFLAGS="%{optflags}" \
    LDFLAGS="%{ldflags}"
popd
%endif

%install
rm -rf %{buildroot}

install -d %{buildroot}{%{_libdir},%{_sysconfdir}/vga}

%makeinstall \
    TOPDIR=%{buildroot} \
    prefix=%{buildroot}%{_prefix} \
    mandir=%{buildroot}%{_mandir} \
    sharedlibdir=%{buildroot}%{_libdir} \
    NO_HELPER=y \
    INSTALL_PROGRAM="install -p -m755" \
    INSTALL_SCRIPT="install -p -m755" \
    INSTALL_SHLIB="install -p -m755" \
    INSTALL_DATA="install -p -m644" \
    INSTALLMODULE="" \
    INSTALLDEV="" \

install -m644 ./src/config/* %{buildroot}%{_sysconfdir}/vga

rm -f %{buildroot}%{_datadir}/{dvorak-us.keymap,libvga.config,libvga.et4000,null.keymap}

%ifarch %{ix86}
# use the newer lrmi stuff
install -m0755 lrmi-0.9/mode3 %{buildroot}%{_bindir}/
install -m0755 lrmi-0.9/vga_reset %{buildroot}%{_bindir}/
%endif

%clean
rm -fr %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc 0-README LICENSE svgalib.lsm
%dir %{_sysconfdir}/vga
%config(noreplace) %{_sysconfdir}/vga/*
%{_bindir}/*
%{_mandir}/man?/*
#%attr(1777,root,root) %dir /var/lib/svgalib

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/CHANGES doc/DESIGN doc/Driver-programming-HOWTO doc/README.joystick doc/README.keymap doc/README.patching doc/README.vesa doc/TODO doc/svgalib.lsm
%{_includedir}/*
#%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man3/*
