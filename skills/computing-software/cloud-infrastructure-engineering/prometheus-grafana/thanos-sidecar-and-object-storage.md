---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-sidecar-and-object-storage
name: thanos-sidecar-and-object-storage
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-sidecar, sidecar-upload, thanos-sidecar-setup, objstore-config, s3, gcs, long-term-storage]
level: advanced
status: docs-checked
description: "Run the Thanos sidecar next to Prometheus: objstore.yml for S3/GCS/Azure, block duration flags, external labels, upload monitoring, and the gotchas that lose blocks."
sources: ["https://thanos.io/tip/components/sidecar.md/", "https://thanos.io/tip/thanos/storage.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos sidecar and object storage

## objstore.yml
```yaml
type: S3
config:
  bucket: metrics-prod
  endpoint: s3.eu-west-1.amazonaws.com
  region: eu-west-1
  # credentials from IRSA / instance profile; or access_key/secret_key
  sse_config: {type: SSE-S3}
---
# GCS
type: GCS
config: {bucket: metrics-prod}          # workload identity or service_account JSON
```

## Prometheus requirements
```
--storage.tsdb.min-block-duration=2h
--storage.tsdb.max-block-duration=2h     # disable local compaction; the Thanos compactor does it
global.external_labels: {cluster: prod-eu, replica: a}   # unique per Prometheus; 'replica' used for dedup
```

## Sidecar
```bash
thanos sidecar \
  --tsdb.path=/prometheus \
  --prometheus.url=http://localhost:9090 \
  --objstore.config-file=/etc/thanos/objstore.yml \
  --grpc-address=0.0.0.0:10901 --http-address=0.0.0.0:10902
```
- Serves the StoreAPI (recent data via Prometheus remote read) to Thanos Query.
- Uploads TSDB blocks as Prometheus produces them (every 2 hours); tracks uploads in `thanos.shipper.json` (`--shipper.meta-file-name`).
- `--shipper.upload-compacted` only for one-time migration of pre-existing compacted blocks.

## Monitor
```promql
time() - thanos_objstore_bucket_last_successful_upload_time > 3 * 3600     # no upload for 3h
```

## Gotchas
- Keep Prometheus retention at least three times the min block duration (6 h) so a bucket outage does not lose blocks; the backlog uploads once connectivity returns.
- Changing external labels creates a new "stream" in the bucket; the compactor treats it as a separate source.
- Two Prometheus replicas both upload; that's expected, deduplicate at query time with `--query.replica-label=replica`.
- Don't run local Prometheus compaction with the sidecar (overlapping blocks halt the compactor).

## Verify
- [ ] `thanos tools bucket ls --objstore.config-file=objstore.yml` lists recent 2 h blocks.
- [ ] Thanos Query `/stores` shows the sidecar healthy with the right label set.

## Checked
- 2026-10-28. Confirmed against the Thanos Sidecar page (2h block production, `--storage.tsdb.min-block-duration=2h` and `--storage.tsdb.max-block-duration=2h`, retention of at least three times the min block duration, `--shipper.upload-compacted` for migration, `thanos.shipper.json`), the Query page (`--query.replica-label`) and the mixin sidecar/storage sources (`thanos_objstore_bucket_last_successful_upload_time`).
- Removed: the Prometheus Operator `spec.thanos` claim, `thanos_shipper_upload_failures_total` and the "1-2 d" retention advice.
Method: documentation only; no commands were run.
