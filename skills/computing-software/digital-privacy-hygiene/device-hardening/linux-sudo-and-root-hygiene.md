---
id: computing-software.digital-privacy-hygiene.device-hardening.linux-sudo-and-root-hygiene
name: linux-sudo-and-root-hygiene
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, sudo-hygiene, linux-hardening, least-privilege, root-account]
level: practitioner
status: draft
description: "Keep Linux desktop privilege tight: lock the root password, audit sudoers and groups, use sudoedit, and avoid running GUI apps or scripts as root."
sources:
  - "https://www.sudo.ws/docs/man/sudoers.man/"
  - "https://wiki.archlinux.org/title/Sudo"
  - "https://ubuntu.com/server/docs"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# sudo and root account hygiene

**Goal:** one user account with deliberate, logged privilege escalation and nothing else.

## Audit
```
getent group sudo wheel admin     # who can escalate
sudo -l                           # what you can run
sudo ls /etc/sudoers.d/           # drop-ins added by packages or old tweaks
sudo passwd -S root               # L = locked
```
Remove users who shouldn't be there: `sudo gpasswd -d <user> sudo`.

## Tighten
- Lock root login: `sudo passwd -l root` (Ubuntu ships this way). Use sudo instead of logging in as root.
- Edit sudoers only with `sudo visudo` (or `visudo -f /etc/sudoers.d/file`) so syntax errors don't lock you out.
- Remove `NOPASSWD` lines unless a specific command truly needs it, and then name the exact command path.
- Shorten the credential cache: `Defaults timestamp_timeout=5`.
- `Defaults use_pty` reduces some terminal injection tricks.

## Habits
- `sudoedit /etc/file` instead of `sudo vim` (editor runs as you).
- Never `curl ... | sudo bash`; download, read, then run.
- Don't run GUI apps (file managers, browsers) with sudo; use polkit prompts (`pkexec`) or admin:// URIs.
- Check logs: `journalctl _COMM=sudo` shows every escalation.

## Gotchas
- Before removing yourself from the sudo group, confirm another way in (root password or second admin user).
- Some distributions use `wheel`, others `sudo`; check `/etc/sudoers` for which group is enabled.
