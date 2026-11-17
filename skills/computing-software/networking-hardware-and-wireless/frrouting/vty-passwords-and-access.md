---
id: computing-software.networking-hardware-and-wireless.frrouting.vty-passwords-and-access
name: vty-passwords-and-access
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, vty, password, enable-password, exec-timeout, access-class, line-vty]
level: practitioner
status: docs-checked
description: "Set FRR vty passwords, enable password, idle timeout and access-class restrictions, and the service commands that change terminal length and password encryption."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VTY passwords and access
- `password PASSWORD` sets the vty password; `no password` deletes it. Without a password a vty will not accept connections.
- `enable password PASSWORD` sets the enable password; the `no` form deletes it.
- `service password-encryption` encrypts passwords.
- `service advanced-vty` enables advanced-mode VTY.
- `service terminal-length (0-512)` sets the system-wide line length for all VTY interfaces; `terminal length (0-512)` sets it for the session. 0 disables display control.

The `line vty` commands are described as deprecated for direct daemon vty access, but can be placed in `frr.conf`:
- `line vty` enters vty configuration mode.
- `exec-timeout MINUTE [SECOND]` sets the idle timeout. Default is 10 minutes; zero (or `0 0`) means no timeout.
- `[ipv6] access-class ACCESS-LIST` restricts vty connections using an IPv4 or IPv6 access list.
- `no vty login` prevents any operator from connecting via the vty.

Daemon-level vty binding uses the common options `-A, --vty_addr <address>` and `-P, --vty_port <port>` (port 0 disables TCP VTY sockets).

In vtysh itself, `-u, --user` blocks entering `en` on the command line, but the docs warn it provides no security or read-only access.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page (password, service, line vty and terminal length commands, invocation options) and the VTY shell page for the -u warning. Nothing changed.
Method: documentation only; no commands were run.
