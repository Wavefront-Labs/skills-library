---
id: computing-software.cybersecurity-defensive.system-hardening.grub-password
name: grub-password
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [grub-password, bootloader-security, grub2, physical-security, linux-hardening, single-user-mode]
level: practitioner
status: docs-checked
description: "Set a GRUB 2 bootloader password so boot entries cannot be edited to get a root shell, keep normal boot unattended, and secure grub.cfg permissions."
sources: ["https://github.com/rhboot/grub2/blob/fedora-46/docs/grub.texi", "https://github.com/systemd/systemd/blob/main/units/rescue.service.in"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GRUB bootloader password

By default anyone with access to the console (physical, IPMI/iDRAC, hypervisor console) can select and edit any GRUB menu
entry and open a GRUB shell prompt (GRUB manual), for example to change the kernel command line and get a root shell
without credentials. A GRUB superuser password blocks editing and the command line.

## Generic method (any distribution)
```bash
grub-mkpasswd-pbkdf2         # grub2-mkpasswd-pbkdf2 on RHEL-family; prints a grub.pbkdf2.sha512.10000.<...> hash
```
Add to `/etc/grub.d/40_custom` (the GRUB manual says grub-mkconfig has no built-in support for authentication and points to this file):
```
set superusers="grubadmin"
password_pbkdf2 grubadmin grub.pbkdf2.sha512.10000.<hash printed by the tool>
```
`superusers` must be set for authentication to be enabled; superusers may use the GRUB command line, edit entries and run any entry. A menu entry defined without `--users` is then restricted to superusers, so normal boot needs `--unrestricted` on the entry (`menuentry "..." --unrestricted { ... }`). How generated entries receive that option depends on your distribution's `/etc/grub.d` scripts; check them. Regenerate `grub.cfg` with `grub-mkconfig` (`grub2-mkconfig` on RHEL-family) or your distribution's wrapper.
Some distributions ship their own helper for setting the password; use your distribution's documentation for it (not checked here).

## Permissions
The plain-text `password` directive makes `grub.cfg` itself sensitive (GRUB manual); keep `grub.cfg` readable by root only regardless.

## Also
- Single-user/rescue mode should require the root password: upstream systemd's `rescue.service` runs `systemd-sulogin-shell rescue`; check what your distribution's unit does.
- UEFI firmware setup password and boot order lock, otherwise an attacker boots from USB instead.
- Full disk encryption (LUKS) protects data at rest; the GRUB password only blocks interactive editing and the GRUB shell.

## Gotchas
- Lose the password and you need rescue media to fix it; store it in the password vault.
- Plaintext `password` directives are possible but never use them; `password_pbkdf2` stores a hash.

## Verify
Reboot, press `e` on the default entry: GRUB prompts for username and password; the default entry boots without
a prompt.

## Checked
Checked 2026-10-25 against the GRUB manual source (`docs/grub.texi` in rhboot/grub2, last commit 2026-10-19; it uses the grub2- command prefixes) and the upstream systemd `units/rescue.service.in`. Confirmed: `superusers`, `password` and `password_pbkdf2`, the hash format prefix `grub.pbkdf2.sha512.10000`, that setting `superusers` restricts the command line and menu-entry editing to superusers, that entries without `--users` are superuser-only unless `--unrestricted`, `/etc/grub.d/40_custom` as the place for authentication, and `rescue.service` using `systemd-sulogin-shell`. Removed unconfirmed: the RHEL `grub2-setpassword` flow and `user.cfg`, the Debian `10_linux` edit, `update-grub`, the `chmod 0600` requirement and cloud console remark. Red Hat documentation and the CIS benchmark were not read.

Method: documentation only; no commands were run.
