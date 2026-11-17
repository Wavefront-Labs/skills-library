---
id: computing-software.systems-network-administration.linux.building-deb-and-rpm-packages
name: building-deb-and-rpm-packages
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, package-building, rpmbuild, spec-file, debuild, dpkg-buildpackage, dpkg-deb, build-from-source, make-install, checkinstall, fpm, nfpm, mock, pbuilder, sbuild, configure-make, destdir, usr-local, stow, alien, rpm-spec, debian-rules, lpic-2, sysadmin, rpmlint, lintian, quilt, rpmmacros]
level: practitioner
status: docs-checked
description: "Build .deb/.rpm instead of make install: rpmbuild spec skeleton and mock, dpkg-buildpackage/debuild layout, fpm/nfpm for quick binary packages, DESTDIR builds and /usr/local discipline."
sources:
  - https://rpm-software-management.github.io/rpm/manual/
  - https://github.com/rpm-software-management/rpm/tree/master/docs/man
  - https://github.com/rpm-software-management/mock/tree/main/docs
  - https://fpm.readthedocs.io/en/latest/
  - https://github.com/goreleaser/nfpm
  - https://manpages.debian.org/stable/dpkg-dev/dpkg-buildpackage.1.en.html
  - https://manpages.debian.org/stable/dpkg/dpkg-deb.1.en.html
  - https://mesonbuild.com/Installing.html
  - https://cmake.org/cmake/help/latest/envvar/DESTDIR.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Building .deb and .rpm packages — ship software the package manager can track

**Goal:** install software so that `dpkg -S`/`rpm -qf` know about every file, upgrades
and removals are clean, and the fleet gets the same binary from a repo instead of a
`make install` done by hand on each host.

## 1. Why not `make install`
`make install` scatters files the package manager cannot see, so a later distro upgrade can
overwrite some of them and `rm` is the only "uninstall". If you must install from source by
hand, keep it out of distro-managed paths (for example a `/usr/local` prefix).

## 2. The quick path: fpm or nfpm (binary → package in one command)
For a Go binary, a tarball of prebuilt files, or a vendor tgz with no build system:
```bash
# fpm (Ruby gem): from a staged directory tree
mkdir -p pkg/usr/bin pkg/lib/systemd/system
cp myapp pkg/usr/bin/; cp myapp.service pkg/lib/systemd/system/
fpm -s dir -t deb -n myapp -v 1.2.0 --iteration 1 -a amd64 \
    --description "My app" --url https://example.com --license MIT \
    --depends 'libc6 (>= 2.31)' \
    --after-install postinst.sh --before-remove prerm.sh \
    --config-files /etc/myapp/config.yml \
    -C pkg .
fpm -s dir -t rpm ... -C pkg .     # same for rpm (needs rpmbuild installed)
```
`nfpm` (Go, YAML config `nfpm.yaml` by default, `nfpm package -p deb`; `-p` picks the packager,
`-f` the config file, `-t` the target) does the same with a declarative file.

## 3. RPM: spec file + `rpmbuild` (+ `mock` for clean builds)
```bash
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
cp myapp-1.2.0.tar.gz ~/rpmbuild/SOURCES/
```
Minimal autotools spec:
```spec
Name:           myapp
Version:        1.2.0
Release:        1%{?dist}
Summary:        My app
License:        MIT
URL:            https://example.com
Source0:        https://example.com/releases/%{name}-%{version}.tar.gz
BuildRequires:  gcc, make
Requires:       openssl-libs
%{?systemd_requires}

%description
Longer description.

%prep
%autosetup                 # unpacks Source0 and applies Patch0..N with -p1

%build
%configure
%make_build

%install
%make_install              # = make install DESTDIR=%{buildroot}
install -D -m 0644 contrib/myapp.service %{buildroot}%{_unitdir}/myapp.service
install -D -m 0640 contrib/config.yml %{buildroot}%{_sysconfdir}/myapp/config.yml

%post
%systemd_post myapp.service
%preun
%systemd_preun myapp.service
%postun
%systemd_postun_with_restart myapp.service

%files
%license LICENSE
%doc README.md
%{_bindir}/myapp
%{_unitdir}/myapp.service
%dir %{_sysconfdir}/myapp
%config(noreplace) %{_sysconfdir}/myapp/config.yml

%changelog
* Wed Oct 15 2026 Build Bot <build@example.com> - 1.2.0-1
- Initial package
```
Build and check:
```bash
rpmbuild -ba ~/rpmbuild/SPECS/myapp.spec       # -bs = source rpm only, -bb = binary only
mock -r <configname> --rebuild ~/rpmbuild/SRPMS/myapp-1.2.0-1.src.rpm   # clean chroot, finds missing BuildRequires
rpm -qpl RPMS/x86_64/myapp-*.rpm; rpm -qp --scripts RPMS/x86_64/myapp-*.rpm
```
Rules that bite: every installed file must be listed in `%files`; `%config(noreplace)` does not
replace a locally modified file; the `Release` bumps on every rebuild of the same version;
`%{?dist}` is the distribution tag. Rebuild an upstream SRPM with a patch: `rpm -i pkg.src.rpm`,
add `Patch0:` + bump Release, `rpmbuild -ba`.

## 4. Debian: `debian/` directory + `dpkg-buildpackage`
The package source needs a `debian/` directory (`control`, `rules`, `changelog`, `copyright`). The
top `debian/changelog` entry sets the version (see `debian-changelog-versioning-with-dch`;
compare versions with `dpkg --compare-versions`).

Build:
```bash
dpkg-buildpackage -us -uc -b        # -b binary only; -us/-uc leave source and changes unsigned; output in ../
dpkg-deb -c ../myapp_1.2.0-1_amd64.deb; dpkg-deb -I ../myapp_1.2.0-1_amd64.deb   # contents, control info
```
For a trivial binary-only deb without the build system: create `myapp/DEBIAN/control` plus the file
tree, then `dpkg-deb --build --root-owner-group myapp`.

## 5. Build from source without packaging (when you really just need a binary)
```bash
./configure --prefix=/usr/local --sysconfdir=/etc && make -j"$(nproc)"
make DESTDIR=/tmp/stage install          # inspect the tree before touching the system
```
`DESTDIR` staging is what both spec `%install` (`%make_install` runs `make install DESTDIR=%{buildroot}`)
and Debian packaging rely on; a build system that ignores `DESTDIR` cannot be packaged cleanly. cmake:
`cmake --install build` honours the `DESTDIR` environment variable; meson: `DESTDIR=/tmp/stage meson install -C build`.

## 6. Distribute
Sign RPMs with `rpmsign --addsign` (the signing key is selected by the `%_gpg_name` macro). Unsigned
packages on a repo with `gpgcheck=1` fail for every client.

## Verify
- [ ] `rpm -qp --scripts` and `rpm -qpl` show the expected scriptlets and files.
- [ ] Install on a clean VM or `mock` chroot; the service starts and
      `rpm -qf`/`dpkg -S` resolve every installed path.
- [ ] Upgrade from the previous version keeps the edited config (`.rpmnew`/conffile
      prompt behaviour) and restarts the service.
- [ ] `rpm -e`/`apt remove --purge` leaves no stray files (`find / -name 'myapp*'`).

## Checked

Checked against the rpm repository docs (rpmbuild(1), rpmsign(1), rpm-spec(5), macros.in, last push 2026-10-22), the systemd repository `macros.systemd.in`, mock docs (index.md and mock.1), fpm `docs/cli-reference.rst`, nfpm source (`internal/cmd/package.go`), dpkg-buildpackage(1) and dpkg-deb(1) (guillemj/dpkg), Meson `Installing.md` and CMake `cmake(1)` and `DESTDIR` docs.
Confirmed: `%autosetup`, `%configure`, `%make_build`, `%make_install` (`make install DESTDIR=%{buildroot}`), `%config(noreplace)`, `%license`, `%systemd_post/preun/postun_with_restart`, `%systemd_requires`, `%{_unitdir}`; `rpmbuild -ba/-bs/-bb` and `--rebuild`; `mock -r <config> --rebuild`; fpm flags `--iteration`, `--depends`, `--after-install`, `--before-remove`, `--config-files`, `-C`, `--license`, `--url`; `nfpm package -p deb` and default `nfpm.yaml`; `dpkg-buildpackage -b/-us/-uc`; `dpkg-deb --build --root-owner-group`, `-c`, `-I`; `cmake --install`, Meson `DESTDIR`.
Fixed: `rpm --addsign` replaced by `rpmsign --addsign`. Removed as unconfirmed: stow, checkinstall and alien remarks, rpmdevtools helpers, rpmlint and lintian, dh_make and debhelper file-by-file details, sbuild and pbuilder, createrepo_c and aptly advice, and the `systemd-rpm-macros` package name.

Method: documentation only; no commands were run.
