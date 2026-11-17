---
id: computing-software.networking-hardware-and-wireless.frrouting.frr-reload-script
name: frr-reload-script
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, frr-reload, config-delta, reload, test, overwrite]
level: practitioner
status: docs-checked
description: "Apply a changed config file to running FRR daemons with frr-reload.py: compute the delta with --test, apply with --reload, and use --daemon, --input and --overwrite."
sources:
  - https://docs.frrouting.org/en/latest/frr-reload.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The frr-reload.py script
It takes a configuration file path, retrieves the running config from the daemons, computes the delta, and runs the vtysh commands needed to apply it. Either `--reload` or `--test` must be given.

- `--test` outputs the delta without applying it.
- `--reload` applies the delta.
- `--input INPUT` uses a file as the running config instead of `show running-config`.
- `--daemon DAEMON` targets one daemon for per-daemon configs; the value must be a keyword vtysh accepts for `show running-config`.
- `--overwrite` rewrites the daemon config file after applying (`frr.conf` for integrated config, `DAEMON.conf` otherwise).
- `--stdout`, `--debug`, `--bindir BINDIR`, `--confdir CONFDIR`, `--vty_socket VTY_SOCKET`.
- `--logfile FILENAME` (default `/var/log/frr/frr-reload.log`); `--rundir RUNDIR` needs write access.

Integrated config is assumed. If each daemon has its own config file the delta can only be computed per daemon, so `--daemon` must be used. Changes are not saved to the config file unless `--overwrite` is given.

The service-level `reload` (`systemctl reload frr`) applies differences between on-disk and running config; see the daemons-file skill.

## Checked

2026-11-04. Confirmed against the FRR frr-reload page and the Basic Setup page (Reloading section). Nothing changed.
Method: documentation only; no commands were run.
