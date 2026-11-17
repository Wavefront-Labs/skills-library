---
id: computing-software.cloud-infrastructure-engineering.graylog.archive-configuration
name: archive-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [archive, restore-archive, archive-backend, enterprise, snapshot-strategy]
level: practitioner
status: docs-checked
description: "Configure Graylog Enterprise archiving of index sets to a backend before retention deletes data, and restore it later."
sources:
  - https://go2docs.graylog.org/current/interacting_with_your_log_data/archiving.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# archive configuration

Archiving stores inactive data cheaply. Archives are written before retention cleaning, so data is not lost. In multi-node deployments only the leader writes archive files. Archived data cannot be searched until restored through the UI.

Prerequisites: Enterprise license, administrator rights, credentials for the storage backend. The Snapshot strategy needs at least one search-cluster node with the search role.

Configure at **Enterprise > Archives > Configuration**: select a backend from the dropdown. Create the backend first if none exists. File system is the default backend, created at first server start; its location is adjustable in Graylog's configuration.

Archive versus Data Lake: both preserve data long term, but a Data Lake retrieves selectively and is generally faster to retrieve from.

## Checked

2026-11-04. Confirmed against the Archiving page and the Data Lake page (retrieval comparison). Nothing removed.

Method: documentation only; no commands were run.
