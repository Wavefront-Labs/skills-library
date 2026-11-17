---
id: computing-software.cloud-infrastructure-engineering.graylog.warm-tier-on-data-node
name: warm-tier-on-data-node
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [warm-tier, node-search-cache-size, s3-repository, gcs-repository, searchable-snapshots]
level: advanced
status: docs-checked
description: "Prepare a Data Node warm tier: repository credentials in datanode.conf, search role, 10 GB cache default and enabling it on index sets."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/create_warm_tier_on_data_node.htm
  - https://go2docs.graylog.org/current/setting_up_graylog/data_node_configuration_file.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# warm tier on data node

Set up a snapshot repository before enabling a warm tier. S3 or GCS buckets are recommended; any supported file system repository also works.

In `datanode.conf` on all search nodes:
- Amazon S3, OVH, SysEleven: `s3_client_default_access_key`, `s3_client_default_secret_key`, `s3_client_default_endpoint`, and `s3_client_default_region` (required for OVH and SysEleven, optional for Amazon S3).
- Google Cloud Storage: `gcs_credentials_file`.
- Azure: `azure_client_default_account` plus a key or SAS token.

Restart all search nodes afterward.

Data Node assigns the search role automatically to any node with a repository backend configured. Each such node reserves 10 GB for the warm tier cache by default; change it with `node_search_cache_size`. The ideal cache size is as large as local storage allows without filling it past 80%.

Then enable the warm tier on new or existing index sets. Self-managed OpenSearch has different steps. The page marks this as a Graylog Enterprise feature.

## Checked

2026-11-04. Confirmed against the Create a Warm Tier on Data Node page (repository keys per backend, automatic search role, 10 GB default cache, node_search_cache_size, restart of search nodes) and the Data Node Configuration Settings Reference. Added the page's 80% fill limit and Enterprise note.

Method: documentation only; no commands were run.
