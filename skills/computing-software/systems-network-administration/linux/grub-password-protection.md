---
id: computing-software.systems-network-administration.linux.grub-password-protection
name: grub-password-protection
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, grub, grub2, grub-password, grub-pbkdf2, grub2-setpassword, bootloader-security, single-user-protection, cis-benchmark, rhcsa, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Stop console users editing kernel arguments (init=/bin/bash, rd.break) by password-protecting GRUB with PBKDF2 hashes, while letting normal entries boot unattended."
sources:
  - https://www.gnu.org/software/grub/manual/grub/grub.html#Authentication-and-authorisation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password-protect GRUB

**Goal:** anyone with console access can still boot the default entries, but editing entries
or the GRUB command line needs a password — closing the "append `rd.break`/`init=/bin/bash`
and reset root" hole. (Physical access still wins: firmware boot from USB, disk removal —
pair with firmware password and LUKS.)

## 1. Generic GRUB
```bash
grub-mkpasswd-pbkdf2              # copy the grub.pbkdf2.sha512.10000.… string
```
```bash
# /etc/grub.d/40_custom  (append)
set superusers="bootadmin"
password_pbkdf2 bootadmin grub.pbkdf2.sha512.10000.<hash>
```
Then regenerate the configuration with `grub-mkconfig`. grub-mkconfig has no built-in support for
authentication; the GRUB manual says to add these commands through `/etc/grub.d/40_custom`.

A menu entry without `--users` can be used only by superusers, so **every** generated entry asks for
the password, including normal boot — usually not wanted on servers. An entry marked `--unrestricted`
can be booted by anyone; the generated entries need that option added by whatever mechanism your
distribution provides for customising its grub.d scripts (re-check after grub package upgrades).

## 2. Users per entry (rare)
`password_pbkdf2 ops <hash>` plus `menuentry "Diag" --users ops { … }` restricts one entry to
listed users; superusers can always edit/boot everything.

## Gotchas
- The plain `password` command uses the password in plain text; always use `password_pbkdf2`.
- If the password is lost, boot from rescue media and remove the lines from `40_custom`, then regenerate the configuration.
- Unattended reboots fail if the default entry is restricted: test a reboot with no
  keyboard interaction before rolling out.
- UEFI systems still allow booting other media unless firmware is locked too.

## Verify
- [ ] At the GRUB menu, pressing `e` or `c` prompts for username/password.
- [ ] Default entry boots with no interaction (reboot unattended).
- [ ] The generated `grub.cfg` contains the `password_pbkdf2` line and never a cleartext password.

## Checked

Documentation check. Checked 2026-10-27 against the GNU GRUB manual source (docs/grub.texi, read from the rhboot/grub2 mirror on 2026-10-27 because gnu.org returned HTTP 429): `set superusers`, `password_pbkdf2`, `grub-mkpasswd-pbkdf2`, `menuentry --users` and `--unrestricted`, that an entry without `--users` is superuser-only, that grub-mkconfig has no built-in authentication support and `40_custom` is the documented route, and that `password` is plain text. Removed the Red Hat `grub2-setpassword` section, the 10_linux CLASS edit, the file modes and the world-readable claim, none of which the GRUB manual covers.
Method: documentation only; no commands were run.
