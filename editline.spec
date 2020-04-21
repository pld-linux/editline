#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Small line editing library without termcap/curses
Summary(pl.UTF-8):	Mała biblioteka do edycji wiersza bez termcap/curses
Name:		editline
Version:	1.17.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	ftp://ftp.troglobit.com/editline/%{name}-%{version}.tar.xz
# Source0-md5:	ec25530e02f0926909bd0f176528019e
URL:		https://troglobit.com/projects/editline/
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a small line editing library. It can be linked into almost any
program to provide command line editing and history functions. It is
call compatible with the FSF readline library, but at a fraction of
the size, and as a result fewer features. It is also distributed under
a much more liberal (BSD) license.

%description -l pl.UTF-8
editline to mała biblioteka do edycji wiersza. Można ją wykorzystać w
prawie każdym programie, aby zapewnić edycję wiersza z funkcją
historii. Jest zgodna co do wywołań z biblioteką FSF readline, ale ma
ułamek jej rozmiaru i w efekcie mniej możliwości. Jest także wydana na
bardziej liberalnej licencji (BSD).

%package devel
Summary:	Header files for editline library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki editline
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for editline library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki editline.

%package static
Summary:	Static editline library
Summary(pl.UTF-8):	Statyczna biblioteka editline
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static editline library.

%description static -l pl.UTF-8
Statyczna biblioteka editline.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies, obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libeditline.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.md LICENSE README.md
%attr(755,root,root) %{_libdir}/libeditline.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeditline.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeditline.so
%{_includedir}/editline.h
%{_pkgconfigdir}/libeditline.pc
# FIXME: conflicts with libedit-devel
#%{_mandir}/man3/editline.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeditline.a
%endif
