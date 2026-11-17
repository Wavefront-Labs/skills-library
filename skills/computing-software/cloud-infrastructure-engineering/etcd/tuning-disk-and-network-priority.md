---
id: computing-software.cloud-infrastructure-engineering.etcd.tuning-disk-and-network-priority
name: tuning-disk-and-network-priority
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [tuning, ionice, tc, disk-priority, network-priority, snapshot-count, cpu-governor, linux]
level: advanced
status: docs-checked
description: "Linux-level tuning for etcd: ionice for disk I/O priority, tc for peer traffic, snapshot-count and CPU governor."
sources:
  - "https://etcd.io/docs/v3.5/tuning/"
  - "https://etcd.io/docs/v3.5/op-guide/performance/"
  - "https://etcd.io/docs/v3.5/faq/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Beyond timeouts, the tuning page lists these knobs.

Disk: if the disk is shared with other workloads, raise etcd's I/O priority on Linux:

```bash
sudo ionice -c2 -n0 -p $(pgrep etcd)
```

(best-effort class, highest priority). The page notes etcd is very sensitive to disk latency: other processes' disk activity can cause long fsync latencies, missed heartbeats, request timeouts and temporary leader loss.

Network: if the leader serves many concurrent client requests, follower peer requests may be delayed, shown as `dropped MsgProp ... since streamMsg's sending buffer is full` on followers. Prioritise peer traffic (port 2380) over client traffic (port 2379) with Linux traffic control (`tc qdisc add ... prio`, then `tc filter` rules); cancel with `tc qdisc del dev eth0 root`.

Snapshots: `--snapshot-count` (default 100000 on the configuration page; the tuning page text says 10,000) is the number of committed transactions that trigger a snapshot to disk. If memory and disk usage are too high, try lowering it, for example `--snapshot-count=5000`.

CPU: etcd is latency sensitive; on Linux set the CPU governor to `performance` (or `conservative`).

Slow-request signal: the FAQ warns `apply entries took too long` when the average apply duration exceeds 100 ms (`--experimental-warning-apply-duration`, default 100ms), usually a slow disk, then CPU starvation.

## Checked

2026-11-03. Confirmed on the v3.5 tuning page: ionice -c2 -n0 example and the effect of disk latency, send-buffer-full messages, tc prio commands and the cancel command, snapshot-count tuning example, CPU governor. Confirmed on the configuration page: --snapshot-count 100000 and --experimental-warning-apply-duration 100ms; the FAQ for the apply entries took too long warning. Noted the tuning page text and configuration page disagree on the snapshot-count default. Removed: the realtime ionice class, since v3.2, WAL-on-own-device, slow fdatasync, and the 8 GiB and hot-key advice (not on these pages).

Method: documentation only; no commands were run.
