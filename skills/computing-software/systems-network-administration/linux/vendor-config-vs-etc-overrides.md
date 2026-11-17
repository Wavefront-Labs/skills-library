---
id: computing-software.systems-network-administration.linux.vendor-config-vs-etc-overrides
name: vendor-config-vs-etc-overrides
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vendor-config, usr-lib-defaults, etc-overrides, drop-in-directories, config-precedence, fhs]
level: practitioner
status: docs-checked
description: "Change configuration without fighting package updates: /usr/lib vendor defaults vs /etc overrides, drop-in precedence, masking, and .rpmnew/.dpkg-dist files."
sources:
  - https://uapi-group.org/specifications/specs/configuration_files_specification/
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  - https://www.freedesktop.org/software/systemd/man/latest/sysctl.d.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-delta.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendor defaults vs /etc overrides

Modern packages (systemd, sysctl, udev, tmpfiles, modprobe and others) ship defaults under `/usr/lib` (or `/usr/share`) and read admin overrides from `/etc`.

## Precedence pattern
`/etc/X.d/` > `/run/X.d/` > `/usr/local/lib/X.d/` > `/usr/lib/X.d/` (the order listed in sysctl.d(5)) — a file in `/etc` with the **same name** replaces the vendor file;
different names are all read in lexical order.
| Thing | Vendor | Admin |
|---|---|---|
| systemd units | `/usr/lib/systemd/system/` | `/etc/systemd/system/` (+ `unit.d/*.conf` drop-ins) |
| sysctl | `/usr/lib/sysctl.d/` | `/etc/sysctl.d/` |
| udev rules | `/usr/lib/udev/rules.d/` | `/etc/udev/rules.d/` |
| tmpfiles | `/usr/lib/tmpfiles.d/` | `/etc/tmpfiles.d/` |
| modprobe | distribution directory (`/usr/lib/modprobe.d/` or `/lib/modprobe.d/`) | `/etc/modprobe.d/` |

## Techniques
- Change one setting: drop-in in `/etc/X.d/99-local.conf` — survives package updates, minimal diff.
- Replace a vendor file entirely: copy to `/etc/...` with the same name and edit.
- Disable a vendor file: symlink the same name in `/etc` to `/dev/null` (`ln -s /dev/null /etc/sysctl.d/<vendor-file>.conf`; `systemctl mask` does this for units).
- See the merged view: `systemd-analyze cat-config sysctl.d`, `systemctl cat <unit>`, `systemd-delta` (finds overridden, masked and extended configuration files).

## Classic /etc files and package updates
When a package's config in `/etc` changed locally and the new package ships a different one:
your package manager keeps one of the two versions and leaves the other beside it with a suffix such as
`.rpmnew`/`.rpmsave` (RPM) or `.dpkg-dist`/`.dpkg-old` (dpkg); see its documentation. Find and merge them after upgrades.

## Gotchas
- Editing files in `/usr/lib` directly is lost at the next update.
- A same-named copy in `/etc` stops receiving vendor fixes forever — prefer drop-ins.

## Verify
- [ ] `systemd-delta` shows your intentional overrides only; no unmerged `.rpmnew`/`.dpkg-dist` files.

## Checked

Checked 2026-10-27 against systemd man pages (systemd-oomd.service, oomd.conf, systemd.resource-control, systemctl, systemd.exec, systemd.unit, sysctl.d, tmpfiles.d, udev, systemd-delta, systemd-analyze), current main, 2026-10-27; kmod modprobe.d(5). Confirmed: search order for sysctl.d, same-name override rule for tmpfiles.d, udev rules directories, modprobe.d directories, systemd-analyze cat-config, systemd-delta purpose. Removed or softened: later-wins wording for conflicting keys, specific lists of other packages using the pattern, example vendor file name, rpmconf and package-manager suffix details.

Method: documentation only; no commands were run.
