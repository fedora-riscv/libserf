%global oname   serf

Name:           libserf
Version:        1.2.1
Release:        3%{?dist}
Summary:        High-Performance Asynchronous HTTP Client Library
License:        ASL 2.0
Url:            http://code.google.com/p/serf
Source0:        https://serf.googlecode.com/files/serf-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  apr-util-devel
BuildRequires:  apr-devel
BuildRequires:  krb5-devel
BuildRequires:  libtool
BuildRequires:  libgssapi-devel
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The serf library is a C-based HTTP client library built upon the Apache 
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       apr-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{oname}-%{version}
sed -i 's|644 $(TARGET_LIB)|755 $(TARGET_LIB)|g' Makefile.in

%build
autoreconf -fiv
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%configure --includedir=%{_includedir}/%{oname}-1 --with-gssapi=%{_prefix}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.*a' -exec rm -f {} ';'

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%doc CHANGES LICENSE NOTICE README design-guide.txt
%{_libdir}/*.so.*

%files devel
%{_includedir}/%{oname}-1/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{oname}*.pc

%changelog
* Mon Jun 19 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-3
- Add support for EPEL6.

* Thu Jun 13 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-2
- Fix the permission of the library.

* Sun Jun 09 2013 Christopher Meng <rpm@cicku.me> - 1.2.1-1
- Initial Package.
