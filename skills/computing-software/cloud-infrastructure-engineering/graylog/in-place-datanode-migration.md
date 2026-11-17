---
id: computing-software.cloud-infrastructure-engineering.graylog.in-place-datanode-migration
name: in-place-datanode-migration
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [in-place-migration, migration-wizard, tls-migration, opensearch-migration, data-node]
level: advanced
status: docs-checked
description: "Migrate an existing self-managed OpenSearch cluster to Data Node in place, including the TLS-secured variant and its conditions."
sources:
  - https://go2docs.graylog.org/current/planning_your_deployment/data_node_in-place_migration.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/tls_enabled_data_node_migration.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# in place datanode migration

In-place migration reuses OpenSearch's existing data directory; data is not copied, and all nodes and indices transition.

Prerequisites: Graylog 6.1 or later; existing self-managed OpenSearch 1.13 or later but no newer than 2.19 (Elasticsearch is unsupported); back up first. Open **System > Cluster Configuration > Data Node Migration** (only shown if not already on Data Node). Page conflict: the TLS guide places the wizard at System > Data Nodes > Data Node Migration. The wizard lists found backends, creates a CA (or accepts your own; skipped if a valid certificate exists), and requires off-UI actions, so read each screen.

TLS-secured clusters use a separate guide. Conditions: Data Node on the same hosts as the OpenSearch nodes, direct (non-container) install, ability to download the Data Node package, a healthy cluster reachable with curl without `-k` (certificate or basic auth), and the exact `securityadmin.sh` command used to secure it. OpenSearch 3.0 or later is not supported for this path. Graylog recommends its internal CA for the new nodes.

## Checked

2026-11-04. Confirmed against the in-place migration guides. Page conflict recorded on the wizard location.

Method: documentation only; no commands were run.
