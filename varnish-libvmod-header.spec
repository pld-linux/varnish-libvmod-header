#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	header
Summary:	A header-modification VMOD for Varnish
Name:		varnish-libvmod-%{vmod}
Version:	0.3
Release:	1
License:	BSD
Group:		Daemons
Source0:	https://github.com/varnish/libvmod-header/archive/3.0/%{vmod}-%{version}.tar.gz
# Source0-md5:	49fef160237d9f4b90b27ef0d11e2552
URL:		https://github.com/varnish/libvmod-header
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-docutils
BuildRequires:	varnish-source
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Varnish Module (vmod) for manipulation of duplicated headers (for
instance multiple Set-Cookie headers).

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libvmod-%{vmod}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man3/vmod_%{vmod}.3*
