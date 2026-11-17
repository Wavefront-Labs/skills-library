---
id: computing-software.systems-network-administration.linux.kernel-network-counters-nstat
name: kernel-network-counters-nstat
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nstat, tcp-retransmits, netstat-s, snmp-counters, listen-overflows, packet-drops, network-troubleshooting]
level: advanced
status: docs-checked
description: "Use kernel SNMP/netstat counters to find network problems: nstat deltas, TCP retransmits, listen queue overflows, SYN cookies, UDP receive errors and socket buffer drops."
sources:
  - https://man7.org/linux/man-pages/man8/nstat.8.html
  - https://docs.kernel.org/networking/snmp_counter.html
  - https://man7.org/linux/man-pages/man8/ss.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nstat and kernel network counters

## Deltas, not totals
```bash
nstat -n ; sleep 10 ; nstat           # first run resets history, second shows changes in 10 s
nstat -az TcpExtListenOverflows TcpExtListenDrops TcpExtSyncookiesSent   # -a absolute values, -z include zero counters
```
## Counters that matter
| Counter | Meaning | Look at |
|---|---|---|
| `TcpExtListenOverflows` / `TcpExtListenDrops` | SYN arrived while the TCP accept queue was full: the kernel drops the SYN and increments both | `somaxconn` (default 4096 since Linux 5.4, caps the listen backlog) and the application's own backlog |
| `TcpExtSyncookiesSent` | SYN cookies were sent | `tcp_max_syn_backlog` (per-listener limit on SYN_RECV requests) |
| `TcpExtTCPAbortOnMemory` | connection aborted because TCP memory ran out while closing | TCP memory limits |
| `IpExtInNoRoutes` | packet dropped: no route found | routing table |
| `IpInAddrErrors` | invalid destination address, or not local with forwarding disabled | `ip_forward` and addressing |

## Pair with per-socket and NIC views
```bash
ss -ti dst 10.0.0.5          # per-connection TCP information
ss -ltn                       # listening sockets
ip -s link show eth0          # interface errors and drops
```

## Verify
- [ ] Problem counter delta returns to ~0 under the same load after the change.

## Checked

Date: 2026-10-25. Documentation release: rtacct(8)/nstat man page (iproute2 mirror, 2026-10-22), Linux kernel Documentation/networking (torvalds/linux master)/snmp_counter.rst and ip-sysctl.rst, read 2026-10-25.
Confirmed: nstat `-n` (update history only), `-a` (absolute values; default is increments since the previous use), `-z` (show zeros); descriptions of TcpExtListenOverflows/ListenDrops, TcpExtSyncookiesSent, TcpExtTCPAbortOnMemory, IpExtInNoRoutes, IpInAddrErrors; `somaxconn` default 4096 (128 before 5.4); `tcp_max_syn_backlog` semantics.
Removed as unconfirmed: TcpRetransSegs, TcpExtTCPTimeouts, TcpExtTCPBacklogDrop, UdpRcvbufErrors and UdpInErrors rows (not described in the kernel counter documentation), the "1-2% sustained" threshold, netstat, softnet_stat and ethtool grep advice.

Method: documentation only; no commands were run.
