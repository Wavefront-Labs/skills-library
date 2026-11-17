---
id: computing-software.digital-forensics-incident-response.volatility.linux-open-files-and-sockets-in-memory
name: linux-open-files-and-sockets-in-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [linux-sockstat, linux-lsof, volatility3, linux-memory-forensics, network-connections, dfir]
level: practitioner
status: docs-checked
description: "List open files and network sockets from Linux memory with Volatility 3 linux.lsof and linux.sockstat: what the plugins report and how to corroborate."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.sockstat.html", "https://volatility3.readthedocs.io/en/latest/volatility3.plugins.linux.lsof.html", "https://man7.org/linux/man-pages/man5/proc.5.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Linux open files and sockets in memory

On a live host, user-space tools can be subverted by a rootkit. From a memory image, Volatility 3 reads
kernel structures directly.

## Plugins
```bash
vol -f mem.lime linux.lsof > lsof.txt
vol -f mem.lime linux.sockstat > sockstat.txt
```
- `linux.lsof` lists open file descriptors per task; its records carry fields such as device, inode and
  access and change times.
- `linux.sockstat` lists all network connections for all processes. Per socket it yields the network
  namespace ID, file descriptor number, family (`AF_UNIX`, `AF_INET`, and so on), socket type
  (`STREAM`, `DGRAM`, and so on), protocol (`UDP`, `TCP`, and so on), and source and destination
  address, port and state.
- Both need a matching kernel symbol table. Use `-h` on each plugin for filter options.

## What to look for
- A shell or interpreter whose standard descriptors 0 to 2 are sockets rather than a terminal or pipe
  (reverse shell pattern); `linux.sockstat` gives the remote address.
- Listeners from unexpected processes or on unexpected ports.
- Raw or packet-family sockets from unexpected processes.
- Compare network namespace IDs when containers are involved.

## Corroborate
- `linux.pslist` and `linux.pstree` for process parentage; `linux.bash` for shell commands.
- Firewall or flow logs for the remote address; EDR network events.
- The proc(5) man page describes the live-system view of file descriptors and sockets the plugins mirror.

## Gotchas
- `linux.sockstat` shows sockets reachable from processes, so sockets that no process holds may not appear.
- A kernel symbol mismatch produces empty or wrong output; check that `linux.pslist` looks sensible first.

## Verify
Each suspicious connection maps to a PID, its command line and binary path, and the remote endpoint appears in
an independent network source or is flagged as memory-only.

## Checked
2026-11-08. Read: sockstat and lsof plugin reference pages (descriptions, yielded fields) and the plugin
module list. Removed unconfirmed claims: exact option names (--pid, --pids, --netns), the AF_NETLINK and
AF_PACKET list, BPFDoor reference, `(deleted)` and `/memfd` path interpretation, TIME_WAIT behaviour, and
older-release statements.
Method: documentation only; no commands were run.
