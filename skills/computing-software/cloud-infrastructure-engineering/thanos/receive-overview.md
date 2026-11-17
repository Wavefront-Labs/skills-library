---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-overview
name: receive-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, remote-write, receiver, push-based]
level: intro
status: docs-checked
description: "Run thanos receive to accept Prometheus remote write, store it in a TSDB and upload blocks."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive overview

`thanos receive` implements the Prometheus Remote Write API. It writes into a local TSDB, uploads blocks to object storage every 2 hours by default, and exposes the StoreAPI so Queriers can read recent data in real time. It suits air-gapped or egress-only environments where only push is possible.

```
thanos receive \
  --tsdb.path "/path/to/receive/data" \
  --grpc-address 0.0.0.0:10907 \
  --http-address 0.0.0.0:10909 \
  --remote-write.address 0.0.0.0:10908 \
  --receive.replication-factor 1 \
  --label 'receive_replica="0"' \
  --receive.local-endpoint 127.0.0.1:10907 \
  --receive.hashrings-file ./data/hashring.json \
  --objstore.config-file bucket.yml
```

Prometheus side:

```yaml
remote_write:
- url: http://<receive-ip>:10908/api/v1/receive
```

**Defaults:** `--remote-write.address=0.0.0.0:19291`, `--tsdb.path=./data`, `--tsdb.retention=15d`. External labels (`--label`) identify the blocks it produces across clusters.

**Exemplars.** Ingested via remote write but discarded by default because `--tsdb.max-exemplars` is 0; set it non-zero to store them per tenant.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
