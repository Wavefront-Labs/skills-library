---
id: computing-software.networking-hardware-and-wireless.frrouting.daemons-file-and-service-control
name: daemons-file-and-service-control
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, daemons-file, systemd, vtysh-enable, network-namespace, service-reload]
level: practitioner
status: docs-checked
description: "Enable FRR daemons in the daemons file, set per-daemon options and file descriptor limits, run in a network namespace, and restart or reload the service."
sources:
  - https://docs.frrouting.org/en/latest/setup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemons file and service control
`/etc/frr/daemons` has a `<name>=no` line per daemon (zebra, bgpd, ospfd, ospf6d, ripd, ripngd, isisd, pimd, ldpd, nhrpd, eigrpd, babeld, sharpd, staticd, pbrd, bfdd, fabricd). Change `no` to `yes`, then restart or reload. After a fresh install nothing runs until daemons are enabled.

- `vtysh_enable=yes` applies configuration via `vtysh -b` at daemon start (recommended).
- `MAX_FDS=1024` sets the descriptor limit; `MAX_<DAEMON>_FDS` overrides it for one daemon, e.g. `MAX_BGPD_FDS=8192`.
- `FRR_NO_ROOT="yes"` runs FRR as a non-root user.
- `<daemon>_options` holds start flags, e.g. `zebra_options=" -s 90000000 --daemon -A 127.0.0.1"`.
- `frr_global_options` is prepended to every daemon's options, e.g. `frr_global_options="-w"`.

Network namespaces: for the default pathspace set `watchfrr_options="--netns=<network-namespace-name>"` in `/etc/frr/daemons`; for a custom pathspace (recommended) use `/etc/frr/<namespace>/daemons` with `watchfrr_options="--netns"` (the namespace name defaults to the pathspace name) and start with `/etc/init.d/frr start <pathspace-name>`.

Service operations: restart (`systemctl restart frr`) stops and starts all daemons and unsaved config is lost; reload (`systemctl reload frr`) applies differences between on-disk and running config and starts newly enabled daemons. Individual daemons cannot be stopped directly; remove their config and set `=no`, then restart.

Run `vtysh` as root, via sudo, or as a user in `frrvty`. Crash logs go to `/var/tmp/frr/<daemon>[-<instance>].<pid>/crashlog`.

## Checked

2026-11-04. Confirmed against the FRR Basic Setup page: daemons list, vtysh_enable, MAX_FDS and MAX_<DAEMON>_FDS, FRR_NO_ROOT, options variables, frr_global_options, namespace setup, restart and reload, crash log path. Added the documented --netns form for a custom pathspace.
Method: documentation only; no commands were run.
