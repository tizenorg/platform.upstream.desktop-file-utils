Name:           desktop-file-utils
Version:        0.20
Release:        0
Summary:        Utilities for Manipulating Desktop Files
License:        GPL-2.0+
Group:          Development/Tools/Other
Url:            http://www.freedesktop.org/wiki/Software/desktop-file-utils
Source0:        http://www.freedesktop.org/software/desktop-file-utils/releases/%{name}-%{version}.tar.xz
Source2:        macros.desktop-file-utils
Source1001:     desktop-file-utils.manifest
BuildRequires:  glib2-devel
BuildRequires:  pkg-config
# Only needed because we don't (and won't) support building xz tarballs by default... See bnc#697467
BuildRequires:  xz

%description
This packages contains a couple of command line utilities for
working with desktop files.

More information about desktop files can be found at:
http://freedesktop.org/wiki/Specifications/desktop-entry-spec

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure \
        --with-lispdir=%{_datadir}/emacs/site-lisp
%__make %{?_smp_mflags}

%install
%makeinstall
# we don't want to buildrequire emacs, but recent automake make it
# impossible to install a lisp file without emacs installed. So we
# manually do it.
test ! -f %{buildroot}%{_datadir}/emacs/site-lisp/desktop-entry-mode.el
install -D -m644 misc/desktop-entry-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/desktop-entry-mode.el
# Install rpm macros
install -D -m644 %{S:2} %{buildroot}%{_sysconfdir}/rpm/macros.desktop-file-utils
# Create ghosts based on default $XDG_DATA_DIRS:
mkdir -p %{buildroot}%{_datadir}/applications
touch %{buildroot}%{_datadir}/applications/mimeinfo.cache

%post
%{_bindir}/update-desktop-database --quiet %{_datadir}/applications || true

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%{_bindir}/desktop-file-edit
%{_bindir}/desktop-file-install
%{_bindir}/desktop-file-validate
%{_bindir}/update-desktop-database
%ghost %{_datadir}/applications/mimeinfo.cache
%{_mandir}/man1/desktop-file-edit.1*
%{_mandir}/man1/desktop-file-install.1*
%{_mandir}/man1/desktop-file-validate.1*
%{_mandir}/man1/update-desktop-database.1*
# Own directories to not require emacs installed.
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*.el*
%{_sysconfdir}/rpm/macros.desktop-file-utils

