---
id: computing-software.cloud-infrastructure-engineering.thanos.receive-hashring-ketama
name: receive-hashring-ketama
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-receive, hashring, ketama, hashmod]
level: advanced
status: docs-checked
description: "Pick the ketama hashring algorithm, migrate from hashmod and use AZ-aware endpoints."
sources: ["https://thanos.io/tip/components/receive.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Receive hashrings and ketama

`--receive.hashrings-algorithm` chooses how series spread over receivers:

- **ketama** (recommended): consistent hashing, so receivers scale without the series churn of hashmod.
- **hashmod** (the flag default for historical reasons, discouraged): adding a node causes churn and memory spikes.

Migrating from hashmod: set up a new receiver pool with ketama hashrings and send remote write to it. Old receivers flush after the retention period and upload blocks; once confirmed, decommission them.

Hashring file (`--receive.hashrings-file`, watched and refreshed, fallback `--receive.hashrings-file-refresh-interval=5m`):

```json
[{"endpoints": [
  {"address": "127.0.0.1:10907", "az": "A"},
  {"address": "127.0.0.1:11907", "az": "B"},
  {"address": "127.0.0.1:12907", "az": "C"}]}]
```

AZ-aware spreading is ketama-only and arrived in v0.32; the array-of-strings endpoint format still works but cannot express zones.

A hashring entry can be limited to tenants with `"tenants": ["foo*"]` and `"tenant_matcher_type": "glob"`.

The Thanos Receive Controller can maintain hashrings automatically in Kubernetes, including when autoscaling with an HPA or Keda.

## Checked

2026-11-03. Confirmed against the Thanos Receive page (components/receive.md) and the Thanos troubleshooting page (operating/troubleshooting.md): hashrings and ketama, shuffle sharding, tenancy and decommissioning, quorum formula, Cap'n Proto, limits and gates, defaults, out-of-bound and out-of-order causes. Added the documented fixes and the out-of-order window flag warnings. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
