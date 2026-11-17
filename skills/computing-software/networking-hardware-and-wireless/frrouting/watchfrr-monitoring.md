---
id: computing-software.networking-hardware-and-wireless.frrouting.watchfrr-monitoring
name: watchfrr-monitoring
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, watchfrr, daemon-restart, show-watchfrr, watchfrr-ignore]
level: intro
status: docs-checked
description: "Check FRR daemon supervision with show watchfrr and stop watchfrr restarting a daemon while debugging with watchfrr ignore."
sources:
  - https://docs.frrouting.org/en/latest/watchfrr.html
  - https://docs.frrouting.org/en/latest/vtysh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WATCHFRR monitoring
WATCHFRR is the daemon that handles failed daemon processes and restarts them as needed. It is started through normal systemd startup and typically needs no end-user management.

- `show watchfrr` gives status information about the daemons WATCHFRR is watching.
- `watchfrr ignore DAEMON` tells WATCHFRR to ignore a specific daemon if it goes unresponsive. This is useful for debugging a working system without WATCHFRR restarting the daemon.

Related: `write integrated` in vtysh writes `frr.conf` through watchfrr and is unavailable if watchfrr is not running. Network-namespace setups pass `--netns=<network-namespace-name>` via `watchfrr_options` in the daemons file.

## Checked

2026-11-04. Confirmed against the FRR WATCHFRR, VTY shell and Basic Setup pages. Nothing changed.
Method: documentation only; no commands were run.
