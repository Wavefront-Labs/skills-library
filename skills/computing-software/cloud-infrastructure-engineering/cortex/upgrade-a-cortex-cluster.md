---
id: computing-software.cloud-infrastructure-engineering.cortex.upgrade-a-cortex-cluster
name: upgrade-a-cortex-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [upgrade, rollout-order, changelog, rollback, ingester-shutdown]
level: advanced
status: docs-checked
description: "Upgrade a Cortex cluster one minor version at a time in the right component order, with ingester draining and downgrade limits."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/operations/upgrading.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Breaking changes are recorded in `CHANGELOG.md` under the target release. Read every `[CHANGE]` entry between your current and target version (not just the target's), and skim `[FEATURE]`, `[ENHANCEMENT]` and `[BUGFIX]`.

Procedure: upgrade one minor version at a time where possible (1.16 to 1.17, not 1.14 to 1.17); patch upgrades can be taken in bulk. Reconcile configuration against the target's Config File Reference, watching renamed or deprecated flags, new required fields and runtime config limits.

Deploy in this order: (1) compactor and store-gateway, (2) querier, query-frontend and query-scheduler, (3) ingester, (4) distributor, (5) ruler and alertmanager. Within stateful sets use rolling updates that respect the ring, draining each pod through the ingester shutdown endpoint so in-memory series flush before termination. After each layer, check dashboards for steady error rates and latency, no new alerts, and sample queries from production tenants; if anything regresses, stop and roll back that layer. Mixed versions across one minor boundary are tolerated; across two minors is not supported.

Ingesters: termination is safe once `cortex_ingester_shipper_uploads_total` stops climbing, and `CortexIngesterHasUnshippedBlocks` means do not terminate yet. Compactor: `CortexBucketIndexNotUpdated` should clear within a compaction interval. Downgrade is supported within a minor version (any patch), but cross-minor downgrade is not.

## Checked

2026-11-04. Claims were read against the Cortex docs page: Upgrading Cortex (see sources). Removed filler and unconfirmed wording.

Method: documentation only; no commands were run.
