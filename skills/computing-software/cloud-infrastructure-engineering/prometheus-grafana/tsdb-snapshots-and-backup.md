---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-snapshots-and-backup
name: tsdb-snapshots-and-backup
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, tsdb-snapshot, prometheus-backup, admin-api, restore, disaster-recovery]
level: practitioner
status: verified
description: "Back up a running Prometheus with the TSDB snapshot admin API (hard links), ship it off-box, and restore it into a fresh data directory."
sources: ["https://prometheus.io/docs/prometheus/latest/querying/api/#snapshot", "https://prometheus.io/docs/prometheus/latest/storage/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB snapshots and backup

## 1. Enable and take a snapshot
The admin API is off by default: start with `--web.enable-admin-api` (protect it, see security model skill).
```bash
curl -s -XPOST 'http://localhost:9090/api/v1/admin/tsdb/snapshot?skip_head=false'
# {"status":"success","data":{"name":"20261016T021500Z-6a2b..."}}
ls /prometheus/data/snapshots/20261016T021500Z-6a2b.../
```
- Snapshot = hard links to every persisted block (`Block.Snapshot` calls `os.Link`), plus (unless `skip_head=true`) a new block
  written from the in-memory head. Near-instant and uses no extra space until compaction rewrites the originals.
- `skip_head=true` is faster and avoids writing a head block, but leaves out everything that is only in the head: on a freshly
  started server it produced an empty snapshot directory.

## 2. Ship it
```bash
SNAP=$(curl -s -XPOST localhost:9090/api/v1/admin/tsdb/snapshot | jq -r .data.name)
tar -C /prometheus/data/snapshots -czf "/backup/$SNAP.tgz" "$SNAP"     # then copy the archive off the host
```
Once the archive is verified, delete the snapshot directory: hard links keep the disk space of blocks that compaction has since
replaced pinned until you do.

## 3. Restore
1. Stop Prometheus (or start a new one).
2. Copy the snapshot contents (the ULID directories) into an empty `--storage.tsdb.path`.
3. Start Prometheus; it loads the blocks; WAL is empty so there is a gap from snapshot time to now.
4. Retention still applies, measured from the newest block (`BeyondTimeRetention` compares each block's end time with the first
   block's): restored blocks older than the retention window are removed once newer blocks sit beside them (a lone restored block
   was kept after 2.5 minutes with `--storage.tsdb.retention.time=1m`). Start with a matching or longer retention.

## Alternatives
- Long-term durable storage is better solved with remote write or Thanos/Mimir; snapshots are for
  migrations, before risky upgrades, and small single-node setups.

## Gotchas
- Forgotten snapshot directories keep replaced blocks' disk space pinned after compaction.
- `--web.enable-admin-api` also enables `delete_series` and `clean_tombstones`; never expose it publicly.
- Snapshots live on the same disk; they are not a backup until copied elsewhere.

## Verify
- [ ] Restore test into a scratch instance answers a query for a timestamp inside the snapshot range.
- [ ] `du -sh data/snapshots` returns to ~0 after the job.
- [ ] Backup job alerts if the newest object in the bucket is older than its schedule.

## Checked
Environment: Windows 11, Prometheus and promtool 3.15.1 (windows-amd64), jq 1.8.2, Git Bash tar.
- Admin API: a server with `--web.enable-admin-api` returned `{"status":"success","data":{"name":"20261022T034817Z-66628a41361df83b"}}` and wrote `snapshots/<name>/<block ULID>/` with `chunks`, `index`, `meta.json`, `tombstones` (head block written); `skip_head=true` on the same fresh server produced an empty directory; a server without the flag answered `admin APIs disabled`.
- Restore: the snapshot's block directory copied into an empty data path of a new server was queryable (`up{job="few"}`, 1,081 series at the time) and the new server created its own `wal/`; `jq -r .data.name` and `tar -czf` ran as written (the archive listed the block).
- Hard links: `Block.Snapshot` in `tsdb/block.go` (prometheus main) uses `os.Link` for meta, index, tombstones and chunks; `DB.Snapshot` writes the head block when `withHead` is true. Retention rule: `BeyondTimeRetention` in `tsdb/db.go`, plus the restored-server test described above.
- Forgotten-snapshot and CSI statements were removed; the `aws s3 cp` step was replaced by a local archive because no cloud account was used.
