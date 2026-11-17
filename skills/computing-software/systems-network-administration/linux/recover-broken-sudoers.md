---
id: computing-software.systems-network-administration.linux.recover-broken-sudoers
name: recover-broken-sudoers
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, sudo, sudoers-recovery, broken-sudoers, visudo, pkexec, rescue-mode, syntax-error]
level: practitioner
status: verified
description: "Recover when sudo fails with 'syntax error in /etc/sudoers' or lost privileges: pkexec visudo, root password, rescue boot or cloud fixes, and preventing it with visudo -c."
sources:
  - https://github.com/sudo-project/sudo/blob/main/docs/visudo.mdoc.in
  - https://github.com/sudo-project/sudo/blob/main/docs/sudoers.mdoc.in
  - https://github.com/systemd/systemd/blob/main/man/systemd.xml
  - https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/copy.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Recovering a broken sudoers

**Symptom:** sudo reports a syntax error in /etc/sudoers or a file under /etc/sudoers.d and refuses to run,
or you removed yourself from the admin group. No sudo = no fix... unless you use another path.

## Ways back in (try in order)
1. **Root password:** `su -` then `visudo -c` and fix (`visudo -f /etc/sudoers.d/90-app`).
2. **Config management/agents** already running as root: Ansible with another privileged account, SSM, Salt.
3. **Rescue boot:** add `systemd.unit=rescue.target` (or `emergency.target`) to the kernel command line from the boot
   loader, fix the file, then continue booting.
4. **Cloud:** serial console or rescue instance (see cloud VM recovery).

## Fix
```bash
visudo -c                       # checks /etc/sudoers and every included file, prints the bad one
visudo -cf /etc/sudoers.d/90-app
chmod 0440 /etc/sudoers.d/90-app; chown root:root /etc/sudoers.d/90-app   # 0440 is the default mode; check ownership and mode
```
Note the include directory skips file names that end in `~` or contain a `.` — renaming to `90-app.bak` disables the file.

## Prevent
- Always edit with `visudo` / `visudo -f` (refuses to save broken syntax).
- Config management: validate before install — the Ansible `copy` and `template` modules accept `validate: /usr/sbin/visudo -cf %s`.
- Keep a second admin path (root password in vault, or a separate sudo rule file never touched by automation).

## Verify
- [ ] `visudo -c` reports no errors for the policy and its included files; `sudo -l` as the admin user lists expected rights.

## Checked
Checked 2026-10-25 against the sudo-project/sudo visudo and sudoers manual sources, systemd(1) (`systemd.unit=`) and the Ansible copy module documentation.
Confirmed: `visudo -c` checks the sudoers file and the files it includes, `-f` selects a file, include-directory skip rule for names ending in `~` or containing `.`, default mode 0440, `systemd.unit=rescue.target` and `emergency.target`, and the Ansible `validate: ... visudo -cf %s` pattern.
Removed as unconfirmed: the exact error text, the polkit route, `init=/bin/bash` and the SELinux autorelabel step, and the `parsed OK` output string.

Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container with sudo 1.9.16p2: visudo -c naming the bad file, line and column; visudo -cf on one file; renaming to .bak or ending in ~ makes the include directory skip the file; /etc/sudoers.d file mode 0440. Not run: rescue.target boot, cloud console recovery, the Ansible validate pattern.
