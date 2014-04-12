%global		_disable_ld_no_undefined	1
%global		module		Blis

Name:		coin-or-%{module}

Summary:	BLIS (BiCePS Linear Integer Solver)
Version:	0.93.11
Release:	2%{?dist}
License:	EPL
URL:		http://projects.coin-or.org/CHiPPS
Source0:	http://www.coin-or.org/download/pkgsource/CHiPPS/%{module}-%{version}.tgz
Source1:	%{name}.rpmlintrc
BuildRequires:	blas-devel
BuildRequires:	bzip2-devel
BuildRequires:	coin-or-Alps-devel
BuildRequires:	coin-or-Bcps-devel
BuildRequires:	coin-or-Cgl-devel
BuildRequires:	coin-or-Clp-devel
BuildRequires:	coin-or-CoinUtils-devel
BuildRequires:	coin-or-Osi-devel
BuildRequires:	doxygen
BuildRequires:	glpk-devel
BuildRequires:	graphviz
BuildRequires:	lapack-devel
BuildRequires:	libatlas-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel
BuildRequires:	texlive-epstopdf
BuildRequires:	zlib-devel

# Properly handle DESTDIR
Patch0:		%{name}-pkgconfig.patch

# Install documentation in standard rpm directory
Patch1:		%{name}-docdir.patch

%description
BLIS (BiCePS Linear Integer Solver) is an application developed on top of
BiCePS and is part of the CHiPPS library hierarchy. BLIS is a branch and cut
solver for Mixed Integer Linear Programs.

%package	devel
Summary:	Development files for %{name}

Requires:	coin-or-CoinUtils-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	doc
Summary:	Documentation files for %{name}

Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
This package contains the documentation for %{name}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1
%patch1 -p1

# silence doxygen deprecation warnings
sed -i 's/^\(SYMBOL_CACHE_SIZE\|SHOW_DIRECTORIES\|HTML_ALIGN_MEMBERS\|USE_INLINE_TREES\|DOT_FONTNAME\)/#\1/g' doxydoc/doxygen.conf.in

%build
mkdir bin; pushd bin; ln -sf %{_bindir}/ld.bfd ld; popd; export PATH=$PWD/bin:$PATH
CFLAGS="%{optflags} -fuse-ld=bfd" CXXFLAGS="%{optflags} -fuse-ld=bfd" \
%configure2_5x
# Kill rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} all doxydoc

%install
export PATH=$PWD/bin:$PATH
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la
cp -a doxydoc/html %{buildroot}%{_docdir}/%{name}

%check
export PATH=$PWD/bin:$PATH
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make test

%files
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/AUTHORS
%doc %{_docdir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README
%doc %{_docdir}/%{name}/blis_addlibs.txt
%{_bindir}/blis
%{_libdir}/*.so.*

%files		devel
%{_includedir}/coin/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files		doc
%doc %{_docdir}/%{name}/html

%changelog
* Thu Mar 20 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.11-2
- Add missing build requires
- Silence doxygen deprecation warnings

* Thu Mar 13 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.11-1
- Update to latest upstream release
- Create doc subpackage

* Mon Jan 14 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.4-4
- Update to run make check (#894610#c4).

* Sat Jan 12 2013 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.3-3
- Rename repackaged tarball.

* Sun Nov 18 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.3-2
- Rename package to coin-or-Blis.
- Do not package Thirdy party data or data without clean license.

* Thu Sep 27 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 0.93.3-1
- Initial coinor-Blis spec.
