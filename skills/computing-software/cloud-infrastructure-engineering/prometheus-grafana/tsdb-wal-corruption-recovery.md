---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-wal-corruption-recovery
name: tsdb-wal-corruption-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, wal, wal-corruption, wal-replay-recovery, crashloop, oomkilled, startup-time]
level: advanced
status: docs-checked
description: "Recover a Prometheus that crashloops on WAL replay: diagnose corruption vs OOM during replay, repair or discard segments, and shorten replay time."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects", "https://prometheus.io/docs/prometheus/latest/command-line/prometheus/", "https://github.com/prometheus/prometheus/blob/main/tsdb/docs/format/wal.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WAL corruption and replay recovery

## 1. Diagnose which failure it is
| Log / symptom | Cause |
|---|---|
| A WAL read error in the log, then a normal start | Torn last record; Prometheus repairs it itself |
| A corruption error naming a segment, then exit | Corruption it cannot repair (disk full mid-write, bad volume) |
| Pod `OOMKilled` during WAL replay (no error) | Replay needs more memory than the limit; not corruption |
| Replay takes very long | Huge WAL (high churn or long head) |
| Lock error on the data directory | Second process on the same directory, or NFS (unsupported) |

## 2. OOM during replay
Replay rebuilds the head series, so it needs a lot of memory.
Raise the limit temporarily (or remove it), let it replay, then fix the cause (cardinality, churn). Recent
versions write head-chunk snapshots on shutdown with
`--enable-feature=memory-snapshot-on-shutdown` so clean restarts skip most replay.

## 3. Unrepairable corruption
```bash
kubectl scale sts prometheus-k8s --replicas=0      # stop it
# on the volume:
ls -la data/wal/            # 00000120 00000121 ... checkpoint.00000119
mkdir /prometheus/wal-quarantine && mv data/wal/00000123 data/wal/00000124 /prometheus/wal-quarantine/
```
- Move the segment named in the error and **every later one**; segments must be contiguous after the checkpoint.
- Losing WAL loses only the not-yet-compacted head (at most ~3 h); persisted blocks are untouched.
- Last resort: move the whole `wal/` and `chunks_head/` aside; Prometheus starts empty for the head.
- A corrupt block (not WAL): move that block directory out of the data directory; Prometheus starts without it.

## 4. Prevent it
- Alert on free disk before the volume fills; a full disk is a common cause.
- `--storage.tsdb.wal-compression` (default since 2.20.0; the WAL size is expected to roughly halve) shrinks WAL and replay IO.
- Use block storage, not NFS/SMB; give the pod a generous termination grace period so it shuts down cleanly.

## Checked
2026-10-31. Confirmed against the Prometheus storage page: blocks are created about every two hours covering the last three hours, `chunks_head/`, `wal/` and `wbl/` directories, `--storage.tsdb.wal-compression` (introduced 2.11.0, default 2.20.0), NFS and non-POSIX filesystems unsupported; and the command-line page lists the `memory-snapshot-on-shutdown` feature. Removed: exact log strings, the 10 minute threshold, metric names and the 300 s grace figure (not in the docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Prometheus logs `TSDB started` and `Server is ready to receive web requests`.
- [ ] No further WAL errors appear in the log after the restart.
- [ ] The gap in graphs matches only the quarantined time span.
