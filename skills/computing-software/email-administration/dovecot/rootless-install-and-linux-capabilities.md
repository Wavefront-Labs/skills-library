---
id: computing-software.email-administration.dovecot.rootless-install-and-linux-capabilities
name: rootless-install-and-linux-capabilities
category: computing-software
field: email-administration
product: dovecot
tags: [rootless, linux-capabilities, non-root, passwd-file, listener-ports, home-install]
level: advanced
status: docs-checked
description: "Run Dovecot as a single non-root user, what to change in settings, and how Linux capabilities preserve chroot and privileged ports."
sources:
  - https://doc.dovecot.org/main/core/config/rootless.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dovecot can run under one system user without root at any point. This is for non-admins who want to run their own mail server, not a security feature. The page compares risk: normal operation has a very small chance of root through Dovecot, a restricted dovecot user chrooted in an empty directory before login, and per-user UIDs after login; rootless has zero chance of root through Dovecot but a mail user who can read everyone's mail if exploited.

Install under the home directory with `./configure --prefix=$HOME/dovecot`, `make`, `make install`, then start `~/dovecot/sbin/dovecot`. An example configuration is installed at `~/dovecot/etc/dovecot/dovecot.conf`.

Linux capabilities let you give selected rights to processes, so you can run rootless without losing chroot or privileged ports. The page lists `setcap` commands: `cap_net_bind_service+ep` on the dovecot binary (privileged ports) and `cap_sys_chroot+ep` on script-login, imap-urlauth-login, submission-login, managesieve-login, pop3-login, imap-login, lmtp and anvil under the libexec directory.

Important settings for a rootless setup:
- Set `default_internal_user`, `default_login_user` and `default_internal_group` to the user and group Dovecot runs as.
- Remove default chrooting (`chroot =` in anvil, imap-login and pop3-login); optional if you use capabilities.
- Change listener ports to unprivileged ones such as 10143, 10993, 10110, 10995; also optional with capabilities.
- Change `log_path` to a location the user can write.
- Use a passwd-file passdb instead of PAM, with a `userdb passwd` block, and a file with a line like `user:{PLAIN}pass` for the login user.

Do not use this where several users need isolation. In that case the per-user UID design gives much stronger separation.

## Checked

2026-11-08. Read the Rootless Installation page in full. Added the build prefix, the exact setcap targets, the named settings (default_internal_user, default_login_user, default_internal_group), chroot, port and log_path changes.

Method: documentation only; no commands were run.
