---
id: computing-software.networking-hardware-and-wireless.frrouting.frr-config-and-saving
name: frr-config-and-saving
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, frr-conf, integrated-config, write-memory, vtysh, running-config]
level: intro
status: docs-checked
description: "Save and load FRR configuration through the single integrated frr.conf with vtysh, and know what hostname and per-daemon files do and do not persist."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
  - https://docs.frrouting.org/en/latest/vtysh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FRR config and saving
FRR uses one integrated file, `/etc/frr/frr.conf`. When started by the init script or systemd, `vtysh` reads it and sends each daemon its portion.

- `write terminal` shows the current configuration on the vty.
- `write file` (also written `write memory`) saves the running configuration to the configuration file.
- `configure [terminal]` enters configuration mode.
- `copy FILENAME running-config` reads a file and processes each line as if typed into vtysh.
- `write integrated` writes `frr.conf` through watchfrr regardless of the `service integrated-vtysh-config` setting; it is unavailable if watchfrr is not running.

Per-daemon files are still read (and `-f`/`--config-file` loads one directly) but are not updated by a write. The docs say to remove them after transition.

Traps:
- Daemons must be running when you save; configuration from daemons that are not running is permanently lost.
- `hostname` and `domainname` apply only to the current vtysh and are not saved even by `write file`. `vtysh.conf` (in `/etc/frr`) is not written by save commands; edit `hostname`, `domainname` and `banner motd` there by hand.
- After restarting any daemon, run `vtysh -b` again to re-apply `frr.conf`.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands and VTY shell pages: integrated frr.conf, write and copy commands, per-daemon file behaviour, hostname and domainname handling, vtysh -b after restarts. Nothing changed.
Method: documentation only; no commands were run.
