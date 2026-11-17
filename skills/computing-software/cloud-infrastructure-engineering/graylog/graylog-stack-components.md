---
id: computing-software.cloud-infrastructure-engineering.graylog.graylog-stack-components
name: graylog-stack-components
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [graylog-stack, data-node-role, mongodb-metadata, architecture, forwarder, sidecar]
level: intro
status: docs-checked
description: "The three mandatory Graylog stack services (Graylog, Data Node, MongoDB), their roles and the optional Forwarder and Sidecar."
sources:
  - https://go2docs.graylog.org/current/planning_your_deployment/the_graylog_stack.htm
  - https://go2docs.graylog.org/current/planning_your_deployment/the_log_lifecycle.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# graylog stack components

The Graylog stack has three mandatory parts:
- **Graylog**: processing and visualization layer. Collects logs, transforms and normalizes them, serves the web interface, search, dashboards and alerting.
- **Data Node**: the search backend. It manages OpenSearch, handles certificate issuance and renewal, manages cluster membership and makes adding nodes easier.
- **MongoDB**: metadata and configuration (users, dashboards, alerts, stream definitions).

Optional components: Graylog Forwarder (remote-site collection) and Graylog Sidecar (central management of collectors).

Data Node is the recommended search backend. Self-managed OpenSearch is possible, but from Graylog 7.0 OpenSearch 1.x is deprecated and will be removed in 8.0.

Log flow: sources send via Forwarders, Sidecar-managed collectors or directly to inputs; processing pipelines transform and route; the Data Node stores and indexes; older or lower-value logs can go to the Data Lake.

## Checked

2026-11-04. Confirmed against the cited page. Nothing removed.

Method: documentation only; no commands were run.
