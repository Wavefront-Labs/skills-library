---
id: computing-software.email-administration.dovecot.chrooting-login-auth-and-mail-processes
name: chrooting-login-auth-and-mail-processes
category: computing-software
field: email-administration
product: dovecot
tags: [chroot, valid-chroot-dirs, mail-chroot, nosuid, auth-chroot, hardlink-setuid]
level: advanced
status: docs-checked
description: "Chroot parts of Dovecot, set valid_chroot_dirs and mail_chroot, return chroot from the userdb, and avoid the setuid hardlink escape."
sources:
  - https://doc.dovecot.org/main/core/config/chrooting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Traditionally the whole server ran in one chroot, which is possible but tricky to set up. Dovecot can chroot different parts separately:
- Login processes (imap-login, pop3-login) are chrooted into an empty non-writable directory by default.
- The auth process can be chrooted with `chroot=<path>` in `service auth` or `service auth-worker`, a good idea if your passdb and userdb need no files outside it.
- Mail processes (imap, pop3) can be chrooted in several ways.

Danger: wrongly used chroots let local users gain root by hardlinking setuid binaries into the jail and tricking them, for example hardlinking `/bin/su` plus a forged `<chroot>/etc/passwd`, or planting a fake `<chroot>/lib/libc.so`. This needs a setuid binary to be runnable in the chroot, which is not possible by default, but mount the filesystem `nosuid` to prevent hardlinked setuid binaries.

Because of this, Dovecot only chroots mail processes into directories listed in `valid_chroot_dirs`. If users may chroot under /var/mail/<user>/ and a home directory tree such as /path/to/userdirs/<user>/, list `/var/mail` and `/path/to/userdirs`.

Selecting the chroot:
- `mail_chroot` chroots every user into one directory.
- The userdb can return a `chroot=<path>` field.
- A `/./` inside the home path marks the chroot point: everything before the `/./` becomes the chroot, so putting it right after `/home` chroots into /home, and putting it at the end of the user's home path chroots into that home directory.

Validate with a test login and check that mail paths still resolve inside the jail.

## Checked

2026-11-03. Confirmed on the Chrooting page: login processes chrooted by default into an empty non-writable directory, chroot=<path> in service auth/auth-worker, mail process chroot options, the setuid hardlink danger (/bin/su plus forged passwd, fake libc.so), nosuid mounts, valid_chroot_dirs, mail_chroot, the userdb chroot field and the /./ home marker. Fixed: examples now use the page's /home paths instead of invented /srv and /path/to/homes paths.

Method: documentation only; no commands were run.
