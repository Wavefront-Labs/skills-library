---
id: computing-software.networking-hardware-and-wireless.frrouting.daemon-common-startup-options
name: daemon-common-startup-options
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, daemon-options, vrf-default-name, network-namespace, modules, limit-fds]
level: advanced
status: docs-checked
description: "Common FRR daemon invocation options: config file, pid file, vty address and port, user, namespace, VRF backend, default VRF name, log, tcli and loadable modules."
sources:
  - https://docs.frrouting.org/en/latest/basic.html
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemon common startup options
- `-d, --daemon` daemon mode; `-f, --config_file <file>`; `-i, --pid_file <file>`.
- `-A, --vty_addr <address>` binds the VTY socket; `-P, --vty_port <port>` (0 disables TCP VTY sockets).
- `-u <user>` user and group to run as.
- `-N <namespace>` appends the namespace to statedir paths.
- `-w, --vrfwnetns` selects the namespace VRF backend; it must match across all daemons.
- `-o, --vrfdefaultname <name>` renames the default VRF (default "default"); must match across daemons. The `frr_global_options` variable in the daemons file is the easiest way to set it.
- `--limit-fds <number>` caps internal file descriptors (default is the system ulimit).
- `--log <stdout|syslog|file:/path>`, `--log-level <level>`, `--command-log-always`, `--tcli` (transactional CLI).
- `-M, --module <module:options>` loads a module at startup. Names without a slash are searched in `/usr/lib/frr/modules`, first with the daemon prefix (e.g. `zebra_mod`). Modules cannot be loaded, reloaded or unloaded at runtime.

Zebra additionally accepts `-b` (parse config and exit), `-K TIME` (sweep zebra-originated routes after TIME seconds), `-r` (keep kernel routes on exit), `-e X` (limit ECMP width), `-s SIZE` (netlink buffer), `--routing-table TABLENO`, and `--nexthop-weight-16-bit`.

## Checked

2026-11-04. Confirmed against the FRR Basic Commands page (Common Invocation Options, Loadable Module Support) and Zebra page (invocation options). Nothing changed.
Method: documentation only; no commands were run.
