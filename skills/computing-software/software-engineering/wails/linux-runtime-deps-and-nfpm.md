---
id: computing-software.software-engineering.wails.linux-runtime-deps-and-nfpm
name: linux-runtime-deps-and-nfpm
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, linux, nfpm, webkit2gtk, gtk3, build-tags, packaging]
level: practitioner
status: docs-checked
description: "Pick GTK3 and WebKit2GTK runtime packages per Linux distro, choose the webkit2_41 or webkit2_40 build tag, and declare them in nfpm."
sources: [https://wails.io/docs/guides/linux-distro-support]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship a Linux Wails app whose users have the right runtime libraries.

## Runtime packages
End users need GTK3 and WebKit2GTK.

| Distro | GTK3 | WebKit2GTK | ABI |
|---|---|---|---|
| Debian 12 / Ubuntu 22.04+ | libgtk-3-0 | libwebkit2gtk-4.1-0 | 4.1 |
| Debian 11 / Ubuntu 20.04 | libgtk-3-0 | libwebkit2gtk-4.0-37 | 4.0 |
| Fedora 40+ | gtk3 | webkit2gtk4.1 | 4.1 |
| RHEL/CentOS/Alma/Rocky 8-9 | gtk3 | webkit2gtk3 | 4.0 |
| openSUSE | libgtk-3-0 | libwebkit2gtk-4_1-0 | 4.1 |
| Arch / Manjaro | gtk3 | webkit2gtk-4.1 | 4.1 |

Install commands follow the distro manager, e.g. `apt install libgtk-3-0 libwebkit2gtk-4.1-0`, `dnf install gtk3 webkit2gtk4.1`, `pacman -S gtk3 webkit2gtk-4.1`.

## Build tag
- `-tags webkit2_41` for ABI 4.1 (default for most modern distros)
- `-tags webkit2_40` for RHEL-based and older Debian/Ubuntu (ABI 4.0)

Notes: Fedora has 4.1 only from version 40; RHEL-family 8-9 has no 4.1; Arch offers both `webkit2gtk` (4.0) and `webkit2gtk-4.1`.

## nfpm dependencies
ABI 4.1 (Debian 12, Ubuntu 22.04+, openSUSE, Arch):

```yaml
depends:
  - libgtk-3-0
  - libwebkit2gtk-4.1-0
overrides:
  rpm:
    depends: [libgtk-3-0, libwebkit2gtk-4_1-0]
  archlinux:
    depends: [gtk3, webkit2gtk-4.1]
```

ABI 4.0 (RHEL family, older Debian/Ubuntu): base `depends: [gtk3, webkit2gtk3]` with `overrides.deb.depends: [libgtk-3-0, libwebkit2gtk-4.0-37]` and `overrides.archlinux.depends: [gtk3, webkit2gtk]`.

Fedora 40+: `depends: [gtk3, webkit2gtk4.1]`.

To support several distros you may need separate nfpm config files per ABI.

Related: `computing-software.software-engineering.wails.file-association-setup` (nfpm packaging example).

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Linux Distro Support" guide.

Corrected or removed: Nothing needed removing; every concrete claim matched the page text.

Method: documentation only; no commands were run.
