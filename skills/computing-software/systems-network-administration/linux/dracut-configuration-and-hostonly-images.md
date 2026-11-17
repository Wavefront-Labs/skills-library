---
id: computing-software.systems-network-administration.linux.dracut-configuration-and-hostonly-images
name: dracut-configuration-and-hostonly-images
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, dracut, initramfs, dracut-conf, dracut-modules, hostonly, dracut-hostonly, add-drivers, lsinitrd, rescue-image, rhel, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Configure dracut through dracut.conf.d: add/omit modules and drivers, choose host-only vs generic images, and rebuild initramfs safely so the system still boots."
sources:
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.conf.5.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/lsinitrd.1.adoc
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dracut configuration: modules, drivers, host-only vs generic

**Goal:** get the drivers and dracut modules you need into the initramfs (storage, network
boot, encryption, RAID) and know when a host-only image will bite you.

## 1. Where configuration lives
- `/usr/lib/dracut/dracut.conf.d/*.conf` — distribution defaults (don't edit); `/run/initramfs/dracut.conf.d/` is also read.
- `/etc/dracut.conf.d/*.conf` — yours; a file with the same name here replaces the one in `/usr/lib`. Files are read in alphanumerical order and override `/etc/dracut.conf`.
- Values are bash-style; list options need **leading and trailing spaces** inside quotes
  so they concatenate cleanly:
```bash
# /etc/dracut.conf.d/50-storage.conf
add_drivers+=" megaraid_sas nvme "
add_dracutmodules+=" mdraid lvm crypt "
omit_dracutmodules+=" plymouth "
install_items+=" /etc/multipath.conf /usr/sbin/mdadm "
compress="zstd"
```
`dracut --list-modules` lists available dracut modules (they live in `/usr/lib/dracut/modules.d`);
`add_dracutmodules` adds to the default set, while `dracutmodules=" ... "` specifies the list of modules to call (rarely what you want). Kernel module names for `add_drivers` are given without the `.ko` suffix.

## 2. Host-only vs generic
| Mode | Contents | Use when |
|---|---|---|
| `hostonly="yes"` (the dracut default, `-H`) | host-specific files and modules for this machine (strictness set by `hostonly_mode`: sloppy or strict) | normal installed system — small, fast |
| `hostonly="no"` | broad driver set | golden images, disks moved to new hardware, P2V/V2V migrations |
If your distribution ships a generic rescue initramfs, keep it as the fallback when the host-only image lacks a new controller's driver.
`hostonly_cmdline` stores host-specific kernel arguments in the image (under `etc/cmdline.d`); unset, it turns on automatically with `hostonly="yes"`, so set `hostonly_cmdline="no"` for images that must boot on other machines.

## 3. Rebuild
```bash
dracut -f                                   # current kernel, default output path
dracut -f /boot/initramfs-$(uname -r).img $(uname -r)
dracut -f --regenerate-all                  # every installed kernel
dracut -f --no-hostonly /boot/initramfs-generic.img $(uname -r)   # one-off generic image
dracut -f --add-drivers "vmw_pvscsi" --kver <kernel-version>
lsinitrd /boot/initramfs-$(uname -r).img | grep -E 'megaraid|mdadm'   # confirm content
lsinitrd -m /boot/initramfs-$(uname -r).img                          # list dracut modules included
```
Always keep the previous image: `cp initramfs-$(uname -r).img{,.bak}` before `-f`.

## Gotchas
- Moving a VM to a different disk controller or hypervisor: a host-only image may lack the
  new disk driver and drop to an emergency shell. Build `--no-hostonly` (or `add_drivers`) **before** migrating.
- Changes in `/etc/dracut.conf.d/` affect only the next rebuild, so a broken config shows up when the image is next regenerated.
- Files needed early (for example multipath.conf or keyfiles) must be listed in `install_items`; host-only mode only picks up what it detects on the running host.

## Verify
- [ ] `lsinitrd` lists the drivers and modules you added.
- [ ] `/boot` still has a working fallback (previous image or rescue entry).
- [ ] Reboot succeeds; `journalctl -b -o short-monotonic | grep dracut` shows no missing-module warnings.

## Checked
Checked 2026-10-25 against the dracut-ng man page sources (dracut-ng/dracut-ng man/*.adoc and doc_site, main as of 2026-10-24; latest release 112). Confirmed: config directories and precedence, list options (`add_drivers`, `add_dracutmodules`, `omit_dracutmodules`, `dracutmodules`, `install_items`, `compress` accepting zstd), `hostonly` as the default with `hostonly_mode` sloppy/strict, `hostonly_cmdline` semantics, dracut options `-f`, `--regenerate-all`, `--no-hostonly`, `--add-drivers`, `--kver`, `--list-modules`, positional `<image> <kernel version>`, and lsinitrd `-m`/`--mod`. Removed unconfirmed claims: distro defaults and rescue image path, kernel-install auto-rebuild, the exact emergency-shell warning text, crypttab handling and the Debian/Ubuntu note.

Method: documentation only; no commands were run.
