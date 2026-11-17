---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovs-ctl-service
name: ovs-ctl-service
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-ctl, ovs-vswitchd, service, start, stop, system-id, daemon, load-kmod]
level: practitioner
status: docs-checked
description: "Start and stop Open vSwitch daemons with ovs-ctl: start, stop, restart, status, version, load-kmod, system-id and delete-bridges options, and common ovs-vswitchd daemon flags."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovs-ctl service control
The man page says ovs-ctl is not meant to be invoked directly by administrators but called by system startup scripts.

Commands: `ovs-ctl --system-id=random|<uuid> [<options>] start`, `stop`, `restart`, `status`, `version`, `load-kmod`, `force-reload-kmod`, `enable-protocol`, `delete-transient-ports`, `help`.
- `start`: loads the kernel module, creates or upgrades the database, starts ovsdb-server, initializes a few database values, optionally deletes bridges and transient ports, then starts ovs-vswitchd. It skips the steps for daemons already running. It succeeds if OVS is already started.
- `stop`: stops ovs-vswitchd and ovsdb-server; does not unload kernel modules; succeeds if they are not running.
- `restart`: stop then start, and saves and restores OpenFlow flows for each bridge.
- `status`: prints whether ovs-vswitchd and ovsdb-server are running; exit status 0 if running, 1 otherwise.
- `version`: runs `ovsdb-server --version` and `ovs-vswitchd --version`.
- `load-kmod`: loads the openvswitch kernel module if not already loaded (also part of `start`).
- `force-reload-kmod`: upgrades the kernel module without rebooting: saves flows, stops the daemons, saves state of OVS internal interfaces (addresses, routes), unloads the module, starts OVS again and restores the state. It warns about daemons (such as the ISC DHCP client on an internal interface) that need a restart. It is an error to give it `--no-ovs-vswitchd`.
- `enable-protocol`: inserts an iptables accept rule for a protocol (`--protocol`, default gre; `--sport`/`--dport` only for tcp or udp) unless iptables is absent or the INPUT chain already has a matching rule.
- `delete-transient-ports`: deletes ports with `other_config:transient` true.

Options for start:
- `--system-id=<uuid>` or `random`: stored in external-ids:system-id of the Open_vSwitch table; should be unique among instances talking to one controller. `random` generates an ID that persists across runs (stored in a file).
- `--system-type`, `--system-version`, `--external-id="<name>=<value>"` (repeatable).
- `--delete-bridges`: delete all bridges after ovsdb-server starts and before ovs-vswitchd starts.
- `--delete-transient-ports`, `--ovs-user=user[:group]` (passes `--user` to both daemons).
- `--no-monitor` (by default `--monitor` is passed to both daemons), `--no-mlockall`, `--no-force-corefiles`, `--no-self-confinement`, `--daemon-cwd`, `--oom-score`, `--ulimit-core`, `--ovsdb-server-priority`/`--ovs-vswitchd-priority` (nice level, default -10), `--ovsdb-server-wrapper`/`--ovs-vswitchd-wrapper` (valgrind, strace, glibc; the first two are not for production).
- File locations: `--db-file`, `--db-sock`, `--db-schema`, `--extra-dbs`.
- `--no-ovsdb-server` and `--no-ovs-vswitchd` stop start, stop and restart from touching that daemon.

Example: `ovs-ctl --system-id=random start`

ovs-vswitchd daemon flags (ovs-vswitchd(8)): `--pidfile[=pidfile]`, `--detach`, `--monitor` (monitor process that restarts the daemon if it dies from a signal indicating a programming error), `--no-chdir`, `--mlockall`, `-v[spec]`/`--verbose`, `--log-file[=file]`, `--unixctl=socket`.

## Checked
2026-11-04. Confirmed against ovs-ctl(8) (commands, options, exit status) and ovs-vswitchd(8) (daemon options). Removed the systemctl advice, the Verify line about `ovs-vsctl show`, and the claim that `force-reload-kmod` "briefly interrupts all datapath forwarding" (the page only says it stops and restarts the daemons); added the status exit codes and other documented behaviour.
Method: documentation only; no commands were run.
