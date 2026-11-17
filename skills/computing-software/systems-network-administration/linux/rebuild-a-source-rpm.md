---
id: computing-software.systems-network-administration.linux.rebuild-a-source-rpm
name: rebuild-a-source-rpm
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, srpm-rebuild, rpmbuild, source-rpm, dnf-builddep, rpmdev-setuptree, mock, patch-a-package]
level: practitioner
status: docs-checked
description: "Rebuild and patch an existing source RPM: download the SRPM, install build deps, rpmbuild --rebuild or edit the spec, bump Release, build in mock and install safely."
sources:
  - https://rpm-packaging-guide.github.io/
  - https://github.com/rpm-software-management/mock/wiki
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Rebuilding a source RPM

**Use cases:** add a patch for a bug not yet fixed upstream, enable a compile option, build a Fedora
package for RHEL/EPEL, rebuild with debugging.

## Quick rebuild (unchanged)
```bash
dnf download --source nginx                   # plugin option --source enables the source repositories of enabled binary repos
dnf builddep nginx-*.src.rpm                  # install what is needed to build the .src.rpm
rpmbuild --rebuild nginx-*.src.rpm            # build binary packages from the source package
```

## Patch it
```bash
rpm -ivh nginx-*.src.rpm                      # installs the spec and sources into the rpmbuild tree
cp fix-bug.patch ~/rpmbuild/SOURCES/
vi ~/rpmbuild/SPECS/nginx.spec
#   Release: 1%{?dist}.local1          <- bump so it is identifiable
#   Patch100: fix-bug.patch
#   %autosetup -p1 applies declared patches (macros.in)
#   %changelog entry
rpmbuild -ba ~/rpmbuild/SPECS/nginx.spec
```
## Clean builds with mock
`mock -r <configname> --rebuild ~/rpmbuild/SRPMS/nginx-*.src.rpm` — builds in a clean chroot (config names such as `fedora-35-x86_64` or `alma+epel-8-x86_64` appear in the mock docs).

## Distributing
Sign the RPMs (`rpmsign --addsign`) and publish them in an internal repo. dnf's `priority` (lowest value wins) and `dnf versionlock` control whether vendor updates replace your build.

## Gotchas
- A vendor update with a higher version-release replaces your build unless locked; watch for upstream fixes.
- `rpmbuild` accepts `--with`/`--without` options for conditional builds (`rpmbuild --rebuild --without <option>`).

## Verify
- [ ] `rpm -qip` on the built RPM shows your Release and changelog; `rpm -V` clean after install.

## Checked

Checked against rpmbuild(1) and rpm(8) (rpm-software-management/rpm docs/man, last push 2026-10-22), dnf-plugins-core download.rst and builddep.rst, macros.in (`%autosetup`) and the mock docs (index.md, mock.1).
Confirmed: `rpmbuild --rebuild`, `--with/--without`, `dnf download --source`, `dnf builddep <.src.rpm>`, `rpmsign --addsign`, `mock -r <config> --rebuild`, dnf `priority` semantics.
Removed as unconfirmed: rpmdevtools helpers, build-as-non-root advice, exact tree layout produced by `rpm -ivh`, the `rhel+epel-9` mock config name, createrepo_c, `%patch -P` syntax.

Method: documentation only; no commands were run.
