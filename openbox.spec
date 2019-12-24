Name:             openbox
Version:          3.6.1
Release:          11
Summary:          Windowmanager based on the original blackbox-code
License:          GPLv2+
URL:              http://openbox.org
Source0:          http://openbox.org/dist/%{name}/%{name}-%{version}.tar.xz
Source1:          http://icculus.org/openbox/tools/setlayout.c
Source2:          xdg-menu
Source3:          menu.xml
Source4:          terminals.menu
Patch1:           openbox-python3.patch

Suggests:         python3-gobject
BuildRequires:    gettext desktop-file-utils pango-devel startup-notification-devel libxml2-devel
BuildRequires:    libXcursor-devel libXt-devel libXrandr-devel libXinerama-devel imlib2-devel libpng-devel
Requires:         python3-pyxdg redhat-menus
Provides:         firstboot(windowmanager)
Obsoletes:        gdm-control < 3.5.2-5 gnome-panel-control < 3.5.2-5 %{name}-gnome < 3.5.2-5
Provides:         %{name}-libs = %{version}-%{release}
Obsoletes:        %{name}-libs < %{version}-%{release}

%description
Openbox is a window manager for the X11 windowing system.
It currently runs on a large list of platforms. It was originally
based on blackbox and currently remains very similar, even using
blackbox styles (with available extensions) for its themeing.

Openbox is the spawn of a number of previous blackbox users/hackers.
Being overall pleased with the window manager, but feeling left unable
to contribute, this project was born.The Openbox project is developed,
maintained, and contributed to by these individuals.

%package     devel
Summary:     Development files for openbox
Requires:    %{name} = %{version}-%{release} pkgconfig pango-devel libxml2-devel glib2-devel

%description devel
This package contains libraries and header files for developing applications that
use openbox.

%package     kde
Summary:     Openbox KDE integration
Requires:    %{name} = %{version}-%{release} plasma-workspace
BuildArch:   noarch

%description   kde
This package provides openbox KDE integration and tools.

%package     help
Summary:     Help documentation for %{name}

%description  help
Man pages and other related help documents for %{name}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%configure --disable-static
sed -ie 's|^hardcode_libdir_flag_spec=.*$|hardcode_libdir_flag_spec=""|g' libtool
sed -ie 's|^runpath_var=LD_RUN_PATH$|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS -o setlayout %{SOURCE1} -lX11

%install
%make_install
install setlayout %{buildroot}%{_bindir}
install -p %{SOURCE2} %{buildroot}%{_libexecdir}/openbox-xdg-menu
sed 's|_LIBEXECDIR_|%{_libexecdir}|g' < %{SOURCE3} > %{buildroot}%{_sysconfdir}/xdg/%{name}/menu.xml

install -m644 -p %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/%{name}/terminals.menu

install -m644 -D data/gnome-session/openbox-gnome.session \
    %{buildroot}%{_datadir}/gnome-session/sessions/openbox-gnome.session
install -m644 -D data/gnome-session/openbox-gnome-fallback.session \
    %{buildroot}%{_datadir}/gnome-session/sessions/openbox-gnome-fallback.session

%find_lang %{name}
%delete_la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS CHANGELOG COMPLIANCE COPYING README
%dir %{_sysconfdir}/xdg/%{name}/
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
%{_bindir}/{%{name},%{name}-session,obxprop,setlayout}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/xsessions/%{name}.desktop
%{_datadir}/themes/*/
%{_libexecdir}/openbox-*
%{_datadir}/applications/*%{name}.desktop
%doc COPYING
%{_libdir}/{libobrender.so.*,libobt.so.*}

%files    devel
%{_includedir}/%{name}/
%{_libdir}/{libobrender.so,libobt.so}
%{_libdir}/pkgconfig/*.pc
%exclude %{_datadir}/doc/%{name}
%exclude %{_datadir}/gnome-session/sessions/openbox-gnome*.session
%exclude %{_datadir}/gnome/wm-properties/openbox.desktop
%exclude %{_mandir}/man1/%{name}-gnome-session*.1*
%exclude %{_bindir}/{gdm-control,gnome-panel-control,%{name}-gnome-session}
%exclude %{_datadir}/xsessions/%{name}-gnome.desktop

%files  kde
%{_bindir}/%{name}-kde-session
%{_datadir}/xsessions/%{name}-kde.desktop

%files  help
%doc data/*.xsd data/menu.xml doc/rc-mouse-focus.xml
%{_mandir}/man1/*

%changelog
* Fri Dec 20 2019 wangzhishun <wangzhishun1@huawei.com> - 3.6.1-11
- Package init
