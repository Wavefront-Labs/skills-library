---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-remote-write-mimir-deduplication
name: prometheus-operator-remote-write-mimir-deduplication
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [mimir-deduplication, replica-label, cluster-label, writerelabelconfigs, grafana-cloud, replicaexternallabelname]
level: advanced
status: docs-checked
description: "Remote-write HA Prometheus or PrometheusAgent pairs to Grafana Mimir or Grafana Cloud with correct cluster and __replica__ labels, including sharded setups."
sources: ["https://prometheus-operator.dev/docs/platform/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mimir and Grafana Cloud accept remote-write samples and deduplicate those from HA pairs if labels are right. Defaults:
- `cluster`: identifies the HA pair; same value on both instances.
- `__replica__`: different for each instance.

## Operator specifics
The operator already sets the external label `prometheus_replica` with the semantic of `__replica__`. Either rename it by setting `.spec.replicaExternalLabelName: __replica__`, or, when the label cannot be changed, use `writeRelabelConfigs` in the `remoteWrite` entry to copy it into `__replica__`. Self-managed Mimir can instead be configured with different deduplication label names.

## Sharded deployments
With multiple shards the `cluster` label must include the shard ID, otherwise shards of one cluster would be deduplicated against each other. The docs show a second variant of the relabel configuration doing exactly that.

The same guidance applies to `PrometheusAgent`.

## Checked

2026-11-08. Read the troubleshooting page in full. Removed an unsourced verification step.

Method: documentation only; no commands were run.
