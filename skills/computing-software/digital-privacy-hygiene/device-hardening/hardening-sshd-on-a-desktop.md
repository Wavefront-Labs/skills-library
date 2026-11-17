---
id: computing-software.digital-privacy-hygiene.device-hardening.hardening-sshd-on-a-desktop
name: hardening-sshd-on-a-desktop
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, sshd-hardening, linux-hardening, ssh, attack-surface]
level: practitioner
status: docs-checked
description: "Turn off the SSH server on a Linux desktop if you don't use it, or restrict it to keys, no root and selected users using sshd_config drop-ins and a config test."
sources:
  - "https://man.openbsd.org/sshd_config"
  - "https://wiki.archlinux.org/title/OpenSSH"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Disabling or hardening sshd on a desktop

**Goal:** no unnecessary listening service; if SSH is needed, only key-based logins from expected places.

## Don't need it
Stop and disable the SSH server service (named sshd.service on Arch; the unit name differs by distribution) or remove
the OpenSSH server package. A server that is not running cannot be attacked.

## Need it: harden
sshd reads /etc/ssh/sshd_config, and on Arch also /etc/ssh/sshd_config.d/*.conf drop-in files. A drop-in such as
/etc/ssh/sshd_config.d/10-hardening.conf can hold:
```
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
AllowUsers alice
X11Forwarding no
```
What each does, per the sshd_config manual: PasswordAuthentication controls password logins (default yes);
KbdInteractiveAuthentication controls keyboard-interactive logins (default yes); PermitRootLogin accepts yes,
prohibit-password, forced-commands-only or no (default prohibit-password); AllowUsers limits logins to listed users
and can appear several times, each instance appending to the list; X11Forwarding defaults to no.

Test before restarting the service: run sshd in test mode (`sshd -t`); a valid configuration produces no output (Arch
wiki). Keep the current session open while you test a new login from another terminal.

## Gotchas
- Unless noted otherwise, for each keyword the first obtained value is used, and Include'd files are processed in
  lexical order. A drop-in that sets `PasswordAuthentication yes` earlier will win over yours; check other files.
- AllowUsers can lock out a key that is correct but belongs to an unlisted account (the Arch wiki lists it as a
  login-failure check).
- Changing the port reduces log noise from automated attempts but does not eliminate them (Arch wiki).

## Checked
Confirmed in the sshd_config manual: first-obtained-value rule, Include glob in lexical order, the defaults and values
of the five keywords above, AllowUsers appending. Confirmed in the Arch wiki: drop-in directory, `sshd -t` test mode,
port-change effect, AllowUsers lockout check. Removed: ss and systemctl commands, the ssh.socket and Ubuntu version
note, ufw firewall rule, VPN advice and the hardware-backed key command, none of which the cited pages state.
Method: docs-only read of cited pages, 2026-11-08
