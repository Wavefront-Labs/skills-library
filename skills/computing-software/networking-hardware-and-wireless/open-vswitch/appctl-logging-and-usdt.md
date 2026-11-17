---
id: computing-software.networking-hardware-and-wireless.open-vswitch.appctl-logging-and-usdt
name: appctl-logging-and-usdt
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-appctl, vlog, logging, usdt, bpftrace, coverage, unixctl, debugging]
level: practitioner
status: docs-checked
description: "Control running OVS daemons with ovs-appctl: vlog/set log levels, coverage and memory counters, and USDT probes with bpftrace or perf."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-appctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
  - https://docs.openvswitch.org/en/latest/topics/usdt-probes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovs-appctl, logging and USDT
ovs-appctl talks to a daemon's control socket:
- `ovs-appctl list-commands`, `ovs-appctl version`.
- `--target`/`-t` picks the daemon (a name resolved through its pidfile in the rundir, or a socket path starting with /); `-T secs` limits runtime (0 or unset waits forever); `-f json --pretty` formats output.
- `vlog/list` shows modules and levels; `vlog/set [spec]` changes them, where spec is words separated by spaces, commas or colons: a module name, a destination (syslog, console or file) and a level (off, emer, err, warn, info, dbg), e.g. `vlog/set <module>:file:dbg`; with no spec it sets every module and destination to dbg; `vlog/reopen` reopens the log file after rotation; `vlog/disable-rate-limit [module]` disables log rate limits (`vlog/enable-rate-limit` re-enables them).
- `coverage/show` and `memory/show` print internal counters.

USDT probes:
- Build with `./configure --enable-usdt-probes`.
- List: `bpftrace -l "usdt:$(which ovs-vswitchd):*"`.
- If the binary is not found by perf: `perf buildid-cache --add $(which ovs-vswitchd)`.
- Probe examples include `dpif_recv:recv_upcall`; ready-made scripts live in `utilities/usdt-scripts/` in the source tree.

Gotcha: file logging happens only if the daemon was started with `--log-file`, whatever level you set for the file destination.

## Checked
2026-11-09. Read in full: ovs-appctl(8) (options, list-commands, version, vlog/list, vlog/set spec rules, vlog/reopen, --log-file note) and docs.openvswitch.org topics/usdt-probes (--enable-usdt-probes, bpftrace -l, perf buildid-cache, utilities/usdt-scripts, dpif_recv:recv_upcall). Checked by name only in ovs-vswitchd(8): vlog/disable-rate-limit, memory/show, coverage/show. Removed: the default-target claim, the runtime-only and log-flooding gotchas, the verify step and the netdev_afxdp example (not in the sources).
Method: documentation only; no commands were run.
