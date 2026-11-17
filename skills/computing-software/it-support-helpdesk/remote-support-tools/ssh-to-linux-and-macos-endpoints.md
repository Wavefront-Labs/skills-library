---
id: computing-software.it-support-helpdesk.remote-support-tools.ssh-to-linux-and-macos-endpoints
name: ssh-to-linux-and-macos-endpoints
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, ssh-support, ssh, openssh, macos-remote-login, linux, jump-host]
level: practitioner
status: draft
description: "Reach Linux and macOS endpoints over SSH for support: enabling Remote Login, key-based auth, jump hosts, debugging with -v, host key changes and keeping work alive."
sources:
  - "https://man.openbsd.org/ssh"
  - "https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac"
  - "https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ssh-to-linux-and-macos-endpoints

## Enable on the endpoint
- Linux: `sudo systemctl enable --now ssh` (Debian/Ubuntu) or `sshd` (RHEL/Fedora); open
  port 22 in `ufw`/`firewalld` only from admin subnets.
- macOS: System Settings > General > Sharing > Remote Login, limited to an admin group.
  At scale, enable via MDM; `systemsetup -setremotelogin on` needs Full Disk Access for the
  calling process on current macOS.
- Windows admins already have the OpenSSH client (`ssh`, `scp`) built in.

## Connect well
```bash
ssh -i ~/.ssh/support_ed25519 admin@host.example.com
ssh -J jump.example.com admin@10.20.30.40      # via bastion
ssh -v admin@host                                # debug auth/negotiation
```
- Keys: `ssh-keygen -t ed25519`, then `ssh-copy-id admin@host` (or append the .pub to
  `~/.ssh/authorized_keys`). Permissions must be `700` on `~/.ssh` and `600` on
  `authorized_keys`, or sshd ignores them.
- Run long jobs inside `tmux` or `screen` so a dropped link does not kill them.

## Reading failures
| Message | Meaning |
|---|---|
| Connection refused | sshd not running or wrong port |
| Connection timed out | firewall / routing |
| Permission denied (publickey) | key not offered or not accepted; `-v` shows which keys were tried |
| REMOTE HOST IDENTIFICATION HAS CHANGED | reinstall or new IP owner; confirm out of band, then `ssh-keygen -R host` |
| Too many authentication failures | agent offering many keys; use `-o IdentitiesOnly=yes -i key` |

## Gotchas
- Never disable host key checking to make the warning go away; it is the man-in-the-middle
  alarm.
- Use per-technician accounts or certificates, not a shared root password.
- macOS privacy (TCC) still applies over SSH; some folders are unreadable until Full Disk
  Access is granted to sshd-keygen-wrapper or via MDM.

## Verify
You can log in with a key as a named account, `sudo -l` shows the expected rights, and
logins appear in `/var/log/auth.log` (Linux) or the unified log (macOS).
