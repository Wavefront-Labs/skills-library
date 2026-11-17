---
id: computing-software.systems-network-administration.linux.apt-source-packages-and-build-dep
name: apt-source-packages-and-build-dep
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, apt, apt-source, apt-build-dep, deb-src, dpkg-buildpackage, dpkg-source, local-patch, backport, debian, ubuntu, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Fetch a Debian/Ubuntu package's source with apt source, install its build dependencies with apt build-dep, apply a patch and rebuild a locally versioned .deb."
sources:
  - https://manpages.debian.org/stable/apt/apt-get.8.en.html
  - https://manpages.debian.org/stable/apt/sources.list.5.en.html
  - https://manpages.debian.org/stable/dpkg-dev/dpkg-buildpackage.1.en.html
  - https://manpages.debian.org/stable/dpkg-dev/dpkg-source.1.en.html
  - https://manpages.debian.org/stable/devscripts/dch.1.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apt source and build-dep

**Goal:** rebuild a distro package with a fix or a changed build option, keep it apt-managed,
and make sure the next official update supersedes it.

## 1. Enable source repositories
Deb822 `.sources` files (sources.list(5)): add `deb-src` to `Types:` in the file under
`/etc/apt/sources.list.d/`:
```
Types: deb deb-src
```
Classic `sources.list`: uncomment or add the `deb-src` lines. A `deb-src` entry is required to fetch source indexes. Then `apt update`.

## 2. Get source and build deps
```bash
apt install build-essential devscripts fakeroot
mkdir ~/build && cd ~/build
apt source nginx                     # fetch the newest source package into the current directory and unpack it
apt build-dep nginx                  # install/remove packages to satisfy the source package's build dependencies
apt source nginx=<version>           # a specific version
apt source --download-only nginx     # fetch without unpacking
```

## 3. Patch and rebuild
```bash
cd nginx-1.24.0
# packages in source format "3.0 (quilt)" keep patches under debian/patches (dpkg-source(1))
dch --local site "Apply local fix for XYZ"       # adds a local suffix to the Debian version (dch(1))
dpkg-buildpackage -us -uc -b                      # -b = binary only; -us/-uc = leave source and changes unsigned
ls ../*.deb
```
Install the resulting `.deb` files from the parent directory with `apt install ./<file>.deb`.

## 4. Keep it under control
- In dpkg version comparison a tilde sorts before anything, even the end of a part (deb-version(5)), so
  a `~` suffix sorts lower than the base version and a `+` suffix sorts higher.
- If the fix must survive updates, `apt-mark hold` it — and track the hold.

## Gotchas
- Without matching `deb-src` lines `apt source` may fetch the wrong (too old or too new) source version or none (apt-get(8)).
- `build-dep` installs and may remove packages on the host; use a container or chroot for throwaway builds.

## Verify
- [ ] `dpkg -s <pkg> | grep Version` shows your local version.
- [ ] `apt-cache policy <pkg>` shows the official candidate will replace it when newer.
- [ ] The patched behaviour is present.

## Checked

Checked against apt-get(8) and sources.list(5) (Debian/apt doc/, last commit 2025-11-10), dpkg-buildpackage(1), dpkg-source(1), deb-version(5) (guillemj/dpkg, 2026-10) and dch(1) on manpages.debian.org (bookworm).
Confirmed: `apt source` fetches the newest version and unpacks, `--download-only`, `pkg=version`, `build-dep` semantics, `deb-src` needed in sources, deb822 `Types: deb deb-src`, `-b`/`-us`/`-uc`, tilde ordering, `dch --local` adds a suffix.
Removed as unconfirmed: Ubuntu/Debian version gates and file names, `apt build-dep ./` with an apt version gate, mk-build-deps, quilt commands, sbuild/pbuilder and lintian advice, aptly/reprepro remark, the example resulting version string.

Method: documentation only; no commands were run.
