---
id: computing-software.database-administration.memcached.troubleshoot-client-timeouts
name: troubleshoot-client-timeouts
category: computing-software
field: database-administration
product: memcached
tags: [timeouts, troubleshooting, mc-conn-tester, syn, conntrack]
level: practitioner
status: docs-checked
description: "Diagnose client timeout errors with mc_conn_tester.pl, firewalls and conntrack limits, swap and load, SYN loss and TIME_WAIT."
sources:
  - https://docs.memcached.org/troubleshooting/timeouts/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Order of checks:
1. Firewalls between client and server: connection-tracking limits drop existing TCP connections.
2. Swap and CPU overload (load average huge with 0% idle); try `nice`/`renice`.
3. Run `mc_conn_tester.pl` (from memcached.org/files) which uses raw ASCII commands, no client:
```
./mc_conn_tester.pl -s memcached-host -p 11211 -c 1000 --timeout 1
```
`Fail: (timeout: 1) (elapsed: ...) (conn: 0) (set: 0) (get: 0)` shows how far a cycle got. Set `$debug = 1` to log all loops.
4. Dropped SYNs: SYN retries are typically 3 s. Run with timeouts 1, 4, 8; if failures shrink as timeout grows, the network drops SYNs.
5. Port exhaustion: `netstat -n | grep -c TIME_WAIT`; check `net.ipv4.ip_local_port_range`, `tcp_max_tw_buckets`, `tcp_fin_timeout`, `tcp_tw_reuse` (the doc's values are examples, not recommendations) and conntrack buckets.

If the tester never fails, suspect the client library.

## Checked

2026-11-04. Confirmed against the Client Timeouts page (firewalls, swap and load, mc_conn_tester.pl usage and output, SYN retry test with timeouts 1/4/8, TIME_WAIT and sysctl examples). Removed: nothing.

Method: documentation only; no commands were run.
