---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-v2-roles
name: jaeger-v2-roles
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, collector-role, query-role, ingester-role, agent-role]
level: intro
status: docs-checked
description: "Choose between Jaeger v2 roles: collector, query, ingester, all-in-one and agent, from one binary."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick a deployment shape.

Jaeger v2 is one binary configured to perform different roles:
- collector: receives trace data from applications and writes it to storage.
- query: serves the APIs and UI.
- ingester: ingests spans from Kafka and writes them to storage; for split collector-Kafka-ingester setups.
- all-in-one: collector and query in one process.
- agent: a host agent or sidecar forwarding to the collector. Jaeger can do it, but the docs recommend the standard OpenTelemetry Collector since you likely need it for metrics and logs too.

Choosing all-in-one versus collector/query is a matter of preference. With an external storage both are horizontally scalable; the split allows separate scaling of read and write traffic and different access and security policies.

All-in-one with in-memory storage suits development and testing only, since data is lost on restart. All-in-one with Badger can be used in production but only for modest data volumes: it is limited to a single instance and cannot scale horizontally.

Failure mode: running all-in-one with in-memory storage in production loses all traces on any restart.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 Architecture page, read in full: the five roles, all-in-one versus collector/query, in-memory and Badger guidance. Removed the claim that collector and query are stateless (not stated on that page).

Method: documentation only; no commands were run.
