---
id: computing-software.data-engineering.snowflake.openflow-and-native-connectors
name: openflow-and-native-connectors
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-openflow, native-connectors, data-ingestion, apache-nifi]
level: advanced
status: docs-checked
description: "Where Snowflake Openflow (managed Apache NiFi) fits among ingestion options, its deployment models, and how to choose between it and Snowpipe."
sources:
  - https://docs.snowflake.com/en/user-guide/data-integration/openflow/about
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Openflow and native connectors

**Goal:** ingest SaaS, database CDC, file and streaming sources into Snowflake with Snowflake-managed tooling instead of a separate EL vendor.

## Openflow
- A managed integration service built on **Apache NiFi**. Snowflake's Snowpipe docs point database and SaaS sources to Openflow connectors; see the Openflow docs for the current connector list.
- Deployment models:
  - **BYOC** (bring your own cloud): runs in your own cloud account; available in AWS Commercial regions.
  - **Snowflake deployments**: available in AWS, Azure and GCP Commercial regions.

## Selection
| Need | Pick |
|---|---|
| DB CDC, data must stay in VPC | Openflow BYOC |
| Low-ops SaaS ingestion | Openflow connector, or a managed EL service if its connector is mature |
| Custom flow logic, routing, many small sources | Openflow (NiFi canvas) |
| Simple files on object storage | Snowpipe / COPY, no Openflow needed |

## Operating
- Least-privilege role per runtime; separate destination schema per source.

## Gotchas
- NiFi flows are powerful and easy to make unmaintainable; prefer stock connectors, version custom flows.
- Connector maturity varies; test schema changes and deletes on the source before relying on one.

## Verify
Insert/update/delete rows at the source; changes land in the destination table within the expected latency.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the Openflow about page: Openflow is Snowflake's integration service built on Apache NiFi; BYOC deployments are available in AWS Commercial regions and Snowflake deployments in AWS, Azure and GCP Commercial regions; Snowpipe docs point database and SaaS sources to Openflow connectors.

Removed: the connector list, data-plane/control-plane description, runtime concepts, Snowpark Container Services claim, the Native Apps connectors section, event-table monitoring claim, NiFi registry and third-party vendor names.

Method: documentation only; no commands were run.
