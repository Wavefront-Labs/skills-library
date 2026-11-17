---
id: computing-software.systems-network-administration.linux.identify-distribution-os-release
name: identify-distribution-os-release
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, os-release, lsb-release, hostnamectl, distribution-detection, id-like, scripting]
level: intro
status: verified
description: "Identify the distribution and version reliably in scripts with /etc/os-release (ID, ID_LIKE, VERSION_ID), hostnamectl, and why lsb_release and /etc/issue are poor sources."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/os-release.html
  - https://www.freedesktop.org/software/systemd/man/latest/hostnamectl.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Identifying the distribution

## /etc/os-release (standard everywhere modern)
```bash
cat /etc/os-release
# fields include NAME, ID, ID_LIKE, VERSION_ID, VERSION_CODENAME, PRETTY_NAME
. /etc/os-release; echo "$ID $VERSION_ID"
```
(`/etc/os-release` takes precedence; if it is missing, read `/usr/lib/os-release`. Either may be a symlink to the other location.)

## Scripting pattern
```bash
. /etc/os-release
case " $ID $ID_LIKE " in
  *" rhel "*|*" fedora "*) pkg="dnf -y install" ;;
  *" debian "*)            pkg="apt-get -y install" ;;
  *" suse "*)              pkg="zypper -n install" ;;
  *" arch "*)              pkg="pacman -S --noconfirm" ;;
  *) echo "unsupported: $ID" >&2; exit 1 ;;
esac
major=${VERSION_ID%%.*}
```
Match on `ID`, falling back to `ID_LIKE` (the documented approach), so derivatives are recognised. Use `PRETTY_NAME` only for display.
`VERSION_CODENAME` carries the release codename where the distribution sets one.

## Other sources
- `hostnamectl` — shows the system hostname and related information.
- `uname -r -m` — kernel and arch only.
- `/etc/redhat-release`, `/etc/debian_version` — distribution-specific files; prefer os-release.
- `lsb_release -a` — not part of os-release; avoid in scripts.
- `/etc/issue` — login banner text, often customised; never parse it.
- Ansible: `ansible_distribution`, `ansible_os_family`, `ansible_distribution_major_version`.

## Verify
- [ ] Script tested against containers of each supported distro (`podman run --rm rockylinux:9 cat /etc/os-release`).

## Checked
2026-10-27. Checked against the systemd os-release(5) and hostnamectl(1) manuals (current systemd main). Confirmed: /etc/os-release takes precedence with /usr/lib/os-release as fallback, ID and ID_LIKE semantics (ID_LIKE examples for centos and ubuntu), the recommendation to use ID, VERSION_ID and ID_LIKE as fallback and PRETTY_NAME for display, VERSION_CODENAME, and the hostnamectl status description. Removed: the sample Rocky output including PLATFORM_ID, the Debian testing VERSION_ID claim, and the lsb_release packaging claim, none of which the manuals cover.

Method: documentation, plus the scripting pattern run 2026-11-01 in rootless containers of ubuntu:24.04 (ID_LIKE debian, codename noble), almalinux:9 (ID_LIKE rhel centos fedora, VERSION_ID 9.8, no codename), fedora (no ID_LIKE, no codename) and alpine (reported unsupported, as designed); /etc/os-release is a symlink to ../usr/lib/os-release in all of them. Not run: hostnamectl and the Ansible facts.
