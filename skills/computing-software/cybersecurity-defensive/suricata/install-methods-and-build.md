---
id: computing-software.cybersecurity-defensive.suricata.install-methods-and-build
name: install-methods-and-build
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [install, packages, source-build, configure]
level: intro
status: docs-checked
description: "Install Suricata from packages or source: supported distributions, build dependencies, configure options and the install-conf, install-rules and install-full targets."
sources: ["https://docs.suricata.io/en/latest/install.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing Suricata

Two routes: source build (most control, verify the source first) or binary packages (Ubuntu PPA, Debian repositories and backports, CentOS/AlmaLinux/RockyLinux/Fedora COPR, Arch and others).

## Source build

1. `./configure` with any options.
2. `make -j8` (adjust the job count).
3. `make install`.

Useful configure options:
- `--disable-gccmarch-native`: portable builds or VMs.
- `--prefix`, `--sysconfdir`, `--localstatedir`: install root, config and log locations.
- `--enable-geoip`, `--enable-dpdk`: optional features.

Dependencies include a C toolchain, Rust and cargo, libjansson, libpcap, libpcre2, libyaml and zlib. On RPM systems enable EPEL and the extra repository first.

## Make targets

- `make install-conf`: creates directories and generates `suricata.yaml`.
- `make install-rules`: downloads the latest Emerging Threats ruleset.
- `make install-full`: both, giving a ready-to-run install.

## Checked

2026-11-04. Every step, option and target above confirmed against the Suricata Installation page.

Method: documentation only; no commands were run.
