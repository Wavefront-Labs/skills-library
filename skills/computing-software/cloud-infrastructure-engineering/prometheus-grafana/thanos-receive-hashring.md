---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-receive-hashring
name: thanos-receive-hashring
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-receive, receive-hashring, receive-router-ingestor, replication-factor, remote-write, multi-tenancy]
level: advanced
status: docs-checked
description: "Deploy Thanos Receive for remote-write ingestion: hashring file, router/ingestor split, replication factor, tenants, the ketama algorithm and scaling without losing writes."
sources: ["https://thanos.io/tip/components/receive.md/", "https://github.com/observatorium/thanos-receive-controller"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos Receive hashring

## Hashring file
```json
[
  {"hashring": "default",
   "endpoints": [
     {"address": "receive-ingestor-0.receive-ingestor:10901", "az": "a"},
     {"address": "receive-ingestor-1.receive-ingestor:10901", "az": "b"},
     {"address": "receive-ingestor-2.receive-ingestor:10901", "az": "c"}]},
  {"hashring": "team-a", "tenants": ["team-a"], "endpoints": ["..."]}
]
```
Tenants route by the `THANOS-TENANT` header (`--receive.tenant-header`); unmatched tenants go to the
hashring without `tenants`.

## Router / ingestor split
```bash
# router: stateless, owns the hashring, forwards
thanos receive --receive.hashrings-file=/etc/thanos/hashrings.json \
  --receive.replication-factor=3 --receive.hashrings-algorithm=ketama \
  --remote-write.address=0.0.0.0:19291 --label=receive="true"
# ingestor: stores TSDB, uploads blocks, serves StoreAPI
thanos receive --receive.local-endpoint=$(POD_NAME).receive-ingestor:10901 \
  --tsdb.path=/var/thanos/receive --objstore.config-file=/etc/thanos/objstore.yml \
  --tsdb.retention=1d --label=replica="$(POD_NAME)"
```
Splitting lets you change the hashring (routers restart) without restarting stateful ingestors.

## Replication and quorum
With `replication-factor=3`, a write succeeds when 2 of 3 replicas ack. Query must deduplicate on the
ingestor `replica` label (`--query.replica-label=replica`). Use `ketama` with `az` set for zone-aware placement (the object endpoint format needs Thanos v0.32 or later).

## Scaling
Changing the endpoint list remaps series. To move from `hashmod` to `ketama`, the Receive page recommends a new pool of receivers with `ketama` hashrings; old receivers flush after their retention period and upload their blocks, then you decommission them.
thanos-receive-controller can generate the hashring file from StatefulSet replicas.

## Monitor
`thanos_receive_forward_requests_total{result="error"}`, `thanos_receive_replications_total{result="error"}`,
`thanos_receive_forward_delay_seconds` (the Receive page points to it when forwarding workers are short) and the mixin's `mixin/alerts/receive` alerts.

## Verify
- [ ] Prometheus remote write shows no failed samples; routers have no forward errors.
- [ ] Killing one ingestor keeps writes succeeding (quorum met).
- [ ] Thanos Query returns deduplicated series across ingestors.

## Checked
- 2026-10-28. Confirmed against the Thanos Receive page (hashring file with `az`, `ketama` and `hashmod`, `THANOS-TENANT` and `--receive.tenant-header`, `--receive.replication-factor`, `--receive.local-endpoint`, `--remote-write.address`, `--tsdb.retention`, quorum, v0.32 for AZ-aware hashrings, hashmod to ketama migration, `thanos_receive_forward_delay_seconds`) and the mixin receive alerts (`thanos_receive_forward_requests_total`, `thanos_receive_replications_total`, quorum `floor((RF+1)/2)`).
- Removed: the "only ~1/N" remap claim, the temporary series-rise claim, `prometheus_tsdb_head_series` and the 503 remark.
Method: documentation only; no commands were run.
