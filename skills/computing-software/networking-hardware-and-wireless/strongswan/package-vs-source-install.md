---
id: computing-software.networking-hardware-and-wireless.strongswan.package-vs-source-install
name: package-vs-source-install
category: computing-software
field: networking-hardware-and-wireless
product: strongswan
tags: [networking-hardware-and-wireless, strongswan, install, distribution-packages, autotools, configure]
level: intro
status: docs-checked
description: "Choose between distribution packages and an Autotools source build of strongSwan, including the Debian swanctl package swap and the sysconfdir and monolithic build options."
sources:
  - https://docs.strongswan.org/docs/latest/install/install.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# package vs source install
Packages exist for Arch, Debian/Ubuntu, openSUSE, Gentoo, Fedora, RHEL/CentOS via EPEL, FreeBSD and Homebrew. Remove distribution packages before building from source.

On Debian/Ubuntu the `strongswan` metapackage installs the legacy starter daemon and backend. To use swanctl/vici instead, install `charon-systemd` and `strongswan-swanctl` and remove `strongswan-starter` and `strongswan-charon`. Keep only one of `charon-systemd` or `strongswan-starter` (or disable one of their units, `strongswan.service` and `strongswan-starter.service`).

Source build (Autotools):

```
wget https://download.strongswan.org/strongswan-x.x.x.tar.bz2
tar xjf strongswan-x.x.x.tar.bz2
cd strongswan-x.x.x
./configure --prefix=/usr --sysconfdir=/etc --<your-options>
make
sudo make install
```

The default prefix is `/usr/local`, so configuration is read from `/usr/local/etc`; use at least `--sysconfdir=/etc`. Check `./configure --help` for the options your release offers. Plugin dependencies need the third-party -dev headers installed. After enabling or disabling plugins run `make clean` before rebuilding.

`--enable-monolithic` builds plugins into their library. Git builds need extra tools; see HACKING in the repository.

## Checked
2026-11-04. Confirmed against the strongSwan Installation Documentation page: package list, Debian/Ubuntu package swap, Autotools steps, default prefix /usr/local, make clean advice, --enable-monolithic, HACKING. Nothing removed.

Method: documentation only; no commands were run.
