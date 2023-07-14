%define beta beta2
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtpositioning
Version:	6.6.0
Release:	%{?beta:0.%{beta}.1}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtpositioning-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtpositioning-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Web Channel module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}SerialPort-devel = %{version}
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	cmake(Qt%{major}Quick)
BuildRequires:	cmake(Qt%{major}Qml)
BuildRequires:	cmake(Qt%{major}QmlModels)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(gypsy)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(geoclue-2.0)
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} Web Channel module

%global extra_files_Positioning \
%dir %{_qtdir}/plugins/position \
%{_qtdir}/plugins/position/libqtposition_geoclue2.so \
%{_qtdir}/plugins/position/libqtposition_gypsy.so \
%{_qtdir}/plugins/position/libqtposition_nmea.so \
%{_qtdir}/plugins/position/libqtposition_positionpoll.so

%global extra_devel_files_Positioning \
%{_qtdir}/lib/cmake/Qt6/FindGconf.cmake \
%{_qtdir}/lib/cmake/Qt6/FindGypsy.cmake \
%{_qtdir}/lib/cmake/Qt6Bundled_Clip2Tri

%global extra_files_PositioningQuick \
%{_qtdir}/qml/QtPositioning

%global extra_devel_files_PositioningQuick \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6positioningquickplugin*.cmake

%qt6libs Positioning PositioningQuick

%package examples
Summary:	Example code demonstrating the use of %{name}
Group:		Development/KDE and Qt

%description examples
Example code demonstrating the use of %{name}

%files examples
%{_qtdir}/examples/positioning

%prep
%autosetup -p1 -n qtpositioning%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
