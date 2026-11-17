---
id: computing-software.systems-network-administration.linux.ss-socket-filters
name: ss-socket-filters
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, ss, ss-filters, ss-listening, iproute2, sockets, netstat-replacement, tcp-states, listening-ports, connection-count, networking, sysadmin, troubleshooting]
level: practitioner
status: docs-checked
description: "Use ss to list listening ports with owning processes, filter by state, port, address and cgroup, read queue and TCP-info columns, and count connections per peer."
sources:
  - https://man7.org/linux/man-pages/man8/ss.8.html
  - https://man7.org/linux/man-pages/man7/tcp.7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ss filters — sockets, states and owners

**Goal:** answer "what is listening", "who is connected", "why is the backlog full" in one
command each, without netstat.

## 1. Listening sockets
```bash
ss -tulpn            # TCP+UDP, listening, process, numeric
ss -ltn 'sport = :443'
ss -ltnp | grep -v 127.0.0.1    # what is exposed beyond loopback
```
When a listener's accept queue is full the kernel drops the SYN and increments `TcpExtListenOverflows` and `TcpExtListenDrops` (`nstat -az TcpExtListenOverflows`); the listen backlog is capped by `net.core.somaxconn`.

## 2. State filters
```bash
ss -tn state established
ss -tn state time-wait | wc -l
ss -tn state syn-recv            # SYN flood or a slow app
ss -tn state close-wait          # app forgot to close() — leak in *your* process
ss -tn exclude established       # everything else
```
Groups: `all`, `connected` (all except listening and closed), `synchronized` (connected except syn-sent), `bucket` (time-wait and syn-recv), `big` (the opposite of bucket), `bound-inactive`.

## 3. Address/port expressions
```bash
ss -tn 'dport = :5432'
ss -tn 'dst 10.0.20.0/24'
ss -tn '( sport = :80 or sport = :443 ) and dst 203.0.113.7'
ss -tn 'sport >= :1024 and sport <= :2048'
ss -tn state established '( dport = :22 )' -o     # -o adds timers (keepalive, retransmit)
```
Quote the whole expression; parentheses need spaces around them.

## 4. More detail
```bash
ss -tni 'dport = :443'       # -i: internal TCP information
ss -tm                        # socket memory (skmem) — find buffers bloating
ss -xp                        # Unix sockets with owners
ss -s                         # summary counts by type/state
ss -tnp --cgroup              # cgroup v2 path of each socket
ss -K 'dport = :6379'         # forcibly close matching sockets (IPv4/IPv6 only; unsupported sockets are skipped silently)
```

## Gotchas
- `*:80` vs `0.0.0.0:80` vs `[::]:80`: a `[::]` listener with `bindv6only=0` also accepts IPv4.
- `-H` suppresses the header and `-O` prints one line per socket; test any script against the exact filter you use, since output columns depend on options.

## Verify
- [ ] `ss -ltnp` lists every expected service with the right bind address and process, and nothing unexpected on 0.0.0.0.
- [ ] A filter like `ss -tn state established 'dport = :5432'` returns the connection count the application reports.

## Checked

Date: 2026-10-25. Documentation release: ss(8) (iproute2 mirror, 2026-10-22), kernel snmp_counter.rst and ip-sysctl.rst (torvalds/linux master), read 2026-10-25.
Confirmed: options `-l -o -i -m -x -p -s -K -H -O --cgroup` and `exclude`; state names and the groups all/connected/synchronized/bucket/big/bound-inactive; listen-queue-full behaviour (SYN dropped, ListenOverflows and ListenDrops incremented); `somaxconn`; `bindv6only` default 0 (IPv4-mapped addresses enabled).
Removed as unconfirmed: Recv-Q/Send-Q meaning for listeners, the awk/sed counting pipeline, the CONFIG_INET_DIAG_DESTROY requirement and iproute2 version, the non-root `-p` behaviour, and the list of TCP info fields.

Method: documentation only; no commands were run.
