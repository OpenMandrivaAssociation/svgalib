%define	name	svgalib
%define	version	1.9.25
%define	major	1
%define	libname	%mklibname %{name} %{major}

Name:		%{name}
Summary:	A low-level fullscreen SVGA graphics library
Version:	%{version}
Release:	%mkrel 2
License:	Public Domain
Group:		System/Libraries
URL:		http://www.svgalib.org/
Source0:	http://www.arava.co.il/matan/svgalib/%{name}-%{version}.tar.gz
#Patch0:		%{name}-1.9.21-norootbuild.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
#%patch0 -p1 -b .peroyvind

%build
%make shared OPTIMIZE="%{optflags}"
#cd sharedlib; ln -s libvgagl.so.%{version} libvgagl.so; ln -s libvga.so.%{version} libvga.so; cd -
cd threeDKit
make OPTIMIZE="%{optflags} -I../gl" LIBS="-L../sharedlib -lm -lvgagl -lvga"
cd -
cd utils
%make OPTIMIZE="%{optflags}"
cd -
%ifarch %{ix86}
cd lrmi-0.9
%make CFLAGS="%{optflags}"
cd -
%endif

%install
rm -rf %{buildroot}
install -d %{buildroot}{%{_libdir},%{_sysconfdir}/vga}
%makeinstall INSTALL_SHLIB="install -c -m755" INSTALLMODULE="" INSTALLDEV="" sharedlibdir=%{buildroot}%{_libdir}
install -m644 ./src/config/* %{buildroot}%{_sysconfdir}/vga

rm -f %{buildroot}%{_datadir}/{dvorak-us.keymap,libvga.config,libvga.et4000,null.keymap}

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
%dir %{_sysconfdir}/vga
%config(noreplace) %{_sysconfdir}/vga/*
%{_bindir}/*
%{_mandir}/man?/*
#%attr(1777,root,root) %dir /var/lib/svgalib
%doc 0-README LICENSE svgalib.lsm

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
#%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man3/*
%doc doc/CHANGES doc/DESIGN doc/Driver-programming-HOWTO doc/README.joystick doc/README.keymap doc/README.patching doc/README.vesa doc/TODO doc/svgalib.lsm


