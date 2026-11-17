---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.monitoring-thanos-and-compactor-halts
name: monitoring-thanos-and-compactor-halts
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos-mixin, compactor-halt, thanos, thanos-compactor, meta-monitoring, thanos-tools-bucket]
level: advanced
status: docs-checked
description: "Monitor Thanos with the mixin alerts and fix the common compactor halt (overlapping or corrupt blocks) with bucket verify, mark and rewrite tools."
sources: ["https://thanos.io/tip/operating/troubleshooting.md/", "https://github.com/thanos-io/thanos/tree/main/mixin", "https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitoring Thanos and compactor halts

## Mixin alerts to load (github.com/thanos-io/thanos/mixin)
`ThanosCompactHalted`, `ThanosCompactMultipleRunning`, `ThanosCompactHasNotRun`, `ThanosSidecarNoConnectionToStartedPrometheus`, `ThanosSidecarBucketOperationsFailed`, `ThanosQueryHttpRequestQueryErrorRateHigh`, `ThanosStoreGrpcErrorRate`, `ThanosReceiveHttpRequestErrorRateHigh`, `ThanosRuleQueueIsDroppingAlerts`. The mixin source is jsonnet (`mixin/alerts/*.libsonnet`); compile it with the mixin tooling in the repo.

## Compactor halt
Symptom: `thanos_compact_halted == 1`, logs "critical error detected; halting". Compaction and downsampling stop; queries over long ranges slow and storage grows.
Common causes:
- Overlapping blocks: two sources with identical external labels (duplicate sidecar, restored Prometheus, OOO data) or missing replica dedup config.
- Corrupt/partial block from an interrupted upload.

## Fix
```bash
# find the issue
thanos tools bucket verify --objstore.config-file=objstore.yml --issues=overlapped_blocks
# inspect blocks and their labels/time ranges
thanos tools bucket inspect --objstore.config-file=objstore.yml
# exclude a block from compaction or delete it (compactor removes after delay)
thanos tools bucket mark --id=<ULID> --marker=no-compact-mark.json --details="overlap with ..." --objstore.config-file=objstore.yml
thanos tools bucket mark --id=<ULID> --marker=deletion-mark.json --details="duplicate" --objstore.config-file=objstore.yml
```
Then restart the compactor. For OOO-created overlaps, enable `--compact.enable-vertical-compaction` (and dedup labels) instead of deleting.

## Other health signals
```promql
thanos_blocks_meta_synced{state="loaded"}     # should keep increasing over days
thanos_objstore_bucket_last_successful_upload_time
rate(thanos_objstore_bucket_operation_failures_total[5m])
```

## Gotchas
- Never run two compactors against the same bucket (`ThanosCompactMultipleRunning` alerts on it); scale out only with label sharding (`--selector.relabel-config`).
- Deleting blocks loses data permanently; snapshot/copy them first if unsure.

## Verify
- [ ] `thanos_compact_halted` back to 0 and `thanos_blocks_meta_synced{state="loaded"}` increasing.
- [ ] Mixin alerts routed to the platform team.

## Checked
- 2026-10-28. Confirmed against the Thanos mixin alert sources (`mixin/alerts/compact`, `sidecar`, `query`, `store`, `receive`, `rule` libsonnet: alert names and the `thanos_compact_halted == 1` rule), the Compact component page (halting behaviour, `thanos_compact_halted`, `--compact.enable-vertical-compaction`, `thanos_blocks_meta_synced`, label sharding) and the Tools page (`bucket verify --issues`, `bucket mark`).
- Fixed: `ThanosCompactIsNotRunning` does not exist in the mixin (the real alert is `ThanosCompactMultipleRunning`).
- Removed: `thanos_compact_todo_compactions`, the prebuilt `alerts.yaml` claim, the `--wait` single-replica remark.
Method: documentation only; no commands were run.
