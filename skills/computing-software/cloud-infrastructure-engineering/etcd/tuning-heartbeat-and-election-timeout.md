---
id: computing-software.cloud-infrastructure-engineering.etcd.tuning-heartbeat-and-election-timeout
name: tuning-heartbeat-and-election-timeout
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [tuning, heartbeat-interval, election-timeout, latency, rtt, leader-election, timeouts, raft]
level: advanced
status: docs-checked
description: "Tune --heartbeat-interval and --election-timeout from measured network round-trip time, with defaults, limits and the same-on-all-members rule."
sources:
  - "https://etcd.io/docs/v3.5/tuning/"
  - "https://etcd.io/docs/v3.5/faq/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd uses a heartbeat from leader to followers and an election timeout after which a follower starts an election.

Defaults: `--heartbeat-interval` 100 ms, `--election-timeout` 1000 ms.

Guidance from the tuning page:

- Heartbeat interval: set to about the maximum round-trip time between members; the recommended range is 0.5 to 1.5 times the RTT. Too small adds CPU and network load; too large delays failure detection.
- Election timeout: at least 10 times the RTT, so that variance does not cause spurious elections. The upper limit is 50000 ms (50 s). The FAQ also says to keep it at least 5 times the heartbeat interval.
- The election timeout is how long a follower goes without a heartbeat before trying to become leader, so a higher value takes longer to detect a leader failure. Both values are in milliseconds.
- Use the same values on all members; different values may disrupt cluster stability.

Examples from the page: with a 10 ms RTT the election timeout should be at least 100 ms. A reasonable RTT for the continental United States is 130 ms and between the US and Japan about 350-400 ms; the 50000 ms upper limit should only be used for globally distributed clusters.

```bash
etcd --heartbeat-interval=100 --election-timeout=500
```

Measure RTT with `ping`. The warning `failed to send out heartbeat on time` appears when the leader skips two heartbeat intervals; the FAQ says it is usually a slow disk (check p99 `wal_fsync_duration_seconds` under 10 ms), then CPU starvation, then a slow network.

## Checked

2026-11-03. Confirmed on the v3.5 tuning page: defaults 100 ms and 1000 ms, heartbeat about the RTT (0.5-1.5x), election timeout at least 10x RTT, 50000 ms upper limit, same values on all members, millisecond units, --heartbeat-interval/--election-timeout example, ping for RTT, 130 ms US and 350-400 ms US-Japan RTTs. Confirmed on the FAQ: 5 x heartbeat guidance and the failed to send out heartbeat on time warning and its causes. Removed: the 1300 ms suggestion, the server is likely overloaded log line and the claim that writes pause for the election timeout.

Method: documentation only; no commands were run.
