---
id: computing-software.cloud-infrastructure-engineering.cortex.ruler-alertmanager-and-configs-api
name: ruler-alertmanager-and-configs-api
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [ruler, alertmanager, configs-api, rules, multi-tenancy]
level: intro
status: docs-checked
description: "Place the optional Cortex ruler, multi-tenant Alertmanager and configs API, including their statefulness and failure behaviour."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The ruler is optional and executes PromQL for recording rules and alerts. It needs a database holding each tenant's rules and alerts. It is semi-stateful and scales horizontally. Running rules hold state and the rulers form a ring. If all rulers fail and restart, alert rules recover: an alert that would have been active within its `for` period is restored to firing. Recording rules, however, will have gaps in the generated series.

The alertmanager is optional. It accepts notifications from the ruler, deduplicates and groups them and routes to receivers such as email, PagerDuty or OpsGenie. It is built on the Prometheus Alertmanager with added multi-tenancy, and also needs a database holding per-tenant configuration. It is semi-stateful: silences and active alerts are persisted to its disk, so if all alertmanager nodes failed at once data would be lost.

The configs API is an optional stateless service to get, set and update ruler and alertmanager configurations in a backend. Supported backends are PostgreSQL and in-memory.

## Checked

Method: docs-checked 2026-11-09 against the Cortex architecture page (raw markdown, read in full). Object-store rule storage was dropped from the ruler paragraph as the page says only "database".
