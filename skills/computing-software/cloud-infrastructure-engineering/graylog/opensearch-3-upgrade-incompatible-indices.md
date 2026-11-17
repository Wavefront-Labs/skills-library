---
id: computing-software.cloud-infrastructure-engineering.graylog.opensearch-3-upgrade-incompatible-indices
name: opensearch-3-upgrade-incompatible-indices
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [opensearch-3, incompatible-indices, data-node-upgrade, snapshot, upgrade]
level: advanced
status: docs-checked
description: "Resolve incompatible indices so Data Node can finish the upgrade to OpenSearch 3.x, with snapshot ordering cautions."
sources:
  - https://go2docs.graylog.org/current/upgrading_graylog/upgrade_to_opensearch_3.x_with_data_node.htm
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/compatibility_matrix.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# opensearch 3 upgrade incompatible indices

Indices created under OpenSearch older than 2.0 are incompatible with 3.x. Graylog notifies you when incompatible indices block the automatic Data Node upgrade.

Before starting: be a Graylog administrator and back up Graylog, MongoDB and Data Node data.

Review status at **System > Cluster Configuration > Data Node Upgrade**. Confirm the cluster health indicator is GREEN; resolve any other status first. Review the Upgrade Data Nodes' embedded OpenSearch section.

Caution: if you archive or delete incompatible indices, snapshots taken before that may not restore on OpenSearch 3.x. Take a new snapshot after resolving incompatible indices and before the upgrade.

Self-managed OpenSearch cannot upgrade to 3.x with incompatible indices present; extra support was planned for a later release. New Graylog installs using 3.x are fine.

## Checked

2026-11-04. Confirmed against the OpenSearch 3.x upgrade page and the Compatibility Matrix. Nothing removed.

Method: documentation only; no commands were run.
