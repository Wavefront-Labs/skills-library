---
id: computing-software.cloud-infrastructure-engineering.graylog.default-service-accounts
name: default-service-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [service-accounts, file-ownership, permissions, linux-users]
level: intro
status: docs-checked
description: "Default Linux service users and groups for Graylog, Forwarder, Sidecar, MongoDB, Data Node and OpenSearch, for ownership troubleshooting."
sources:
  - https://go2docs.graylog.org/current/setting_up_graylog/default_users_and_groups.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# default service accounts

Typical user:group values on standard package installs (defaults may vary by platform):
- Graylog core service: `graylog:graylog`
- Graylog Forwarder: `graylog-forwarder:graylog-forwarder`
- Graylog Sidecar: `graylog-sidecar:graylog-sidecar`
- MongoDB: `mongod:mongod`
- Graylog Data Node: `graylog-datanode:graylog-datanode`
- OpenSearch: `opensearch:opensearch` (only with self-managed OpenSearch, not Data Node)

Use these when diagnosing start-up failures caused by wrong ownership or permissions on data, journal, config and log directories. Administrative (root or sudo) access is required to change them.

## Checked

2026-11-04. Confirmed against the cited page. Nothing removed.

Method: documentation only; no commands were run.
