---
id: computing-software.networking-hardware-and-wireless.frrouting.vtysh-usage-and-options
name: vtysh-usage-and-options
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, vtysh, vtysh-conf, pager, exec-timeout, ping, traceroute]
level: practitioner
status: docs-checked
description: "Use the vtysh shell: integrated config service setting, vtysh.conf, -b -w -T options, pager, terminal monitor, exec-timeout and built-in ping and traceroute."
sources:
  - https://docs.frrouting.org/en/latest/vtysh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vtysh usage and options
Access: vtysh uses sockets in `/var/run/frr` and requires membership in the `frrvty` group.

Options: `-b` processes `frr.conf` and applies it to the daemons; `-w` writes the integrated configuration directly (run as superuser or the FRR user); `-T, --exec-timeout` sets idle timeout in seconds; `-u, --user` blocks `en` on the command line without providing real security.

`service integrated-vtysh-config` (set in `vtysh.conf`):
- set: vtysh always writes `frr.conf`;
- `no` form: vtysh never writes it and asks daemons to write their own files;
- neither: writes `frr.conf` if it exists, otherwise uses the daemons.

Other commands:
- `terminal monitor [DAEMON]` shows log messages at debug priority on stderr; some may be lost if vtysh falls behind.
- `terminal paginate` toggles pagination (intended for `vtysh.conf`).
- `exec-timeout TIMEOUT` exits vtysh after idle seconds; zero means none.
- `username USERNAME nopassword` skips PAM for that user, if built with PAM.
- `ping [ip|ipv6] DESTINATION [source SOURCE] [count COUNT] [dontfragment]` (COUNT 1-1000; runs until interrupted without it).
- `traceroute [ip|ipv6] DESTINATION`; `mtrace SOURCE [GROUP]` via `mtracebis`.

Environment: `VTYSH_PAGER` pipes all output through the given program; unset, vtysh uses `more`. The page recommends `less -EFX`.

## Checked

2026-11-04. Confirmed against the FRR VTY shell page: sockets and frrvty group, -b -w -T -u options, service integrated-vtysh-config states, terminal monitor and paginate, VTYSH_PAGER, exec-timeout, username nopassword, ping, traceroute and mtrace. Nothing changed.
Method: documentation only; no commands were run.
