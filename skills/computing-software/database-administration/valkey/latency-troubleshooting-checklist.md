---
id: computing-software.database-administration.valkey.latency-troubleshooting-checklist
name: latency-troubleshooting-checklist
category: computing-software
field: database-administration
product: valkey
tags: [latency, troubleshooting, slowlog, intrinsic-latency, valkey-cli-latency, slow-commands, keys]
level: practitioner
status: docs-checked
description: "Valkey latency checklist: slowlog, intrinsic latency baseline, network and Unix socket latency, slow commands, KEYS avoidance and durability vs latency tradeoffs."
sources:
  - https://valkey.io/topics/latency/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Latency here means the maximum delay from command issue to reply. Quick checklist:
1. Check for blocking slow commands with the Slow Log (`SLOWLOG`).
2. On EC2 use modern HVM instances, or `fork()` is too slow.
3. Disable transparent huge pages (`echo never > /sys/kernel/mm/transparent_hugepage/enabled`) and restart.
4. In VMs measure intrinsic latency with `./valkey-cli --intrinsic-latency 100` on the server (100 = seconds; it saturates one core and does not connect to Valkey).
5. Enable the latency monitor.

Measure round trips with `valkey-cli --latency -h host -p port`. Intrinsic latency is a floor you cannot beat: the page shows 115 microseconds on a healthy host, 9.7 ms on a loaded VM, and up to 40 ms seen elsewhere.

Network: about 200 us on 1 Gbit/s, as low as 30 us over a Unix domain socket. Keep connections long-lived, use Unix sockets on the same host, prefer `MSET`/`MGET` and variadic commands over pipelining, pipelining over separate round trips, and Lua when a reply feeds the next command. Never pin Valkey to a single core: `BGSAVE` and `BGREWRITEAOF` children must not share the event-loop core.

Execution is mostly single-threaded, so one slow command stalls everyone. Complex commands (`SORT`, `LREM`, `SUNION`, big set intersections) should not hit large values; run them on a replica. `KEYS` in production is a very common cause: use `SCAN`, `SSCAN`, `HSCAN`, `ZSCAN`.

Durability vs latency, safest to fastest: AOF fsync always; AOF everysec; everysec plus `no-appendfsync-on-rewrite yes`; AOF never fsync; RDB.

## Checked
2026-11-03. Confirmed against the Valkey latency diagnosis page (valkey.io/topics/latency/): the five-point checklist, the durability ordering, `valkey-cli --latency`, `--intrinsic-latency 100` (seconds, runs on the server, saturates a core, no server connection), the 115 microsecond, 9.7 ms and 40 ms figures, 200 us on 1 Gbit/s versus 30 us on a Unix socket, the client guidelines, the single-core warning for BGSAVE/BGREWRITEAOF, slow commands and `KEYS` versus the SCAN family. The page carries an under-review notice. Nothing removed.
Method: documentation only; no commands were run.
