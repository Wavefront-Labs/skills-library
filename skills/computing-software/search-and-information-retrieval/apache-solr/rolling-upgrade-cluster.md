---
id: computing-software.search-and-information-retrieval.apache-solr.rolling-upgrade-cluster
name: rolling-upgrade-cluster
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [upgrade, rolling-upgrade, upgrade-solr, overseer, upgrade-checklist, cluster-upgrade]
level: advanced
status: docs-checked
description: "Upgrade a SolrCloud cluster with a rolling restart: pre-checks, Overseer leader last, healthy replicas only, noting ZK_HOST, SOLR_HOST_ADVERTISE, SOLR_PORT, SOLR_HOME."
sources:
  - https://solr.apache.org/guide/solr/latest/deployment-guide/upgrading-a-solr-cluster.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rolling-upgrade-cluster

For clusters installed with the service scripts, with default service name `solr` (adjust paths if not).

Checklist before starting:
- Read the Solr Upgrade Notes for behavior changes.
- If any collection is not replicated, back it up first. If all are replicated, each node is upgraded and verified individually.
- Find the Overseer leader with the Overseer Status API and upgrade that node last.
- Choose a maintenance window if possible; the process is a one-by-one rolling restart.
- Verify the cluster is healthy and all replicas are active; never upgrade a degraded cluster.
- Rebuild and test custom server-side components against the new Solr JARs.
- Record per-node values: `ZK_HOST` (same for all nodes), `SOLR_HOST_ADVERTISE` (the registered host), `SOLR_PORT`, and `SOLR_HOME`, which is passed as `solr.solr.home`.

The `IndexUpgraderTool` is not needed in the vast majority of upgrade workflows. Upgrade, restart and confirm each node is healthy and its replicas are active before moving to the next.

## Checked

2026-11-04. Confirmed against Upgrading a Solr Cluster: pre-upgrade checklist, Overseer leader last, per-node values `ZK_HOST`, `SOLR_HOST_ADVERTISE`, `SOLR_PORT`, `SOLR_HOME`, `IndexUpgraderTool` note. Nothing removed.

Method: documentation only; no commands were run.
