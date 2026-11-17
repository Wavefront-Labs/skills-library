---
id: computing-software.cloud-infrastructure-engineering.azure.data-factory-pipelines-and-data-integration
name: data-factory-pipelines-and-data-integration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, data-factory, adf, data-pipelines, data-integration, synapse, synapse-pipelines, stream-analytics, databricks, linked-services, datasets, integration-runtime, self-hosted-integration-runtime, managed-vnet, copy-activity, mapping-data-flows, triggers, tumbling-window, event-trigger, incremental-load, watermark, change-data-capture, pipeline-monitoring, adf-git, adf-cicd, key-vault-linked-service, managed-identity-adf]
level: practitioner
status: docs-checked
description: "Build data integration on Azure: Data Factory vs Synapse vs Databricks vs Stream Analytics, integration runtimes, Copy/Data Flow, incremental loads, triggers, Git CI/CD."
sources: ["https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-performance-features", "https://learn.microsoft.com/en-us/azure/data-factory/control-flow-for-each-activity", "https://learn.microsoft.com/en-us/azure/data-factory/control-flow-lookup-activity", "https://learn.microsoft.com/en-us/azure/data-factory/concepts-integration-runtime", "https://learn.microsoft.com/en-us/azure/data-factory/managed-virtual-network-private-endpoint"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Data Factory and data integration — pipelines that move data privately, incrementally, by Git

**Goal:** batch and streaming integration built on the right engine, running inside
private networks with managed identities, loading only what changed, deployed from a
repo and observed like any other production system.

## 1. Which engine
| Need | Use |
|---|---|
| Orchestration + copy between many sources/sinks, low-code transforms | **Data Factory** (or Synapse pipelines in a Synapse workspace) |
| Heavy transforms in Spark/SQL, notebooks, ML, Delta Lake | **Databricks** (ADF orchestrates a notebook/job activity) or Synapse Spark |
| Streaming from Event Hubs/IoT Hub with SQL-like queries and windowing | **Stream Analytics** (or Spark Structured Streaming) |
| Warehouse | A SQL warehouse engine, not ADF's job |
Push heavy transformation logic to Databricks or SQL; use Mapping Data Flows for medium transforms.

## 2. Factory setup
```bash
az datafactory create -g rg-data -n adf-prod --location uksouth --public-network-access Disabled
az datafactory integration-runtime self-hosted create -g rg-data --factory-name adf-prod -n ir-onprem   # then install the self-hosted IR with the auth key
az datafactory managed-private-endpoint create -g rg-data --factory-name adf-prod --managed-virtual-network-name default -n pe-sql --group-id sqlServer --private-link-resource-id <sql-server-id>   # approve on the target
```
- **Integration runtimes**: *Azure IR*, *Azure IR in a managed virtual network* (private, with **managed private endpoints**), *Self-hosted IR* (Windows only; install on an on-premises machine or a VM in a private network, scale out by associating several machines in active-active mode), *Azure-SSIS IR* for SSIS packages. In Data Factory all outbound ports are open when you use the Azure IR.
- Credentials: use the factory **managed identity** on Azure sources/sinks and a **Key Vault linked service** for the rest; never secrets in linked-service JSON.

## 3. Pipelines that scale
- **Copy activity**: `dataIntegrationUnits` (DIUs) allowed range is 4 to 256; leave it on Auto (service picks by source-sink pair and data pattern) unless tuning. `parallelCopies` is the maximum number of threads reading or writing in parallel and must be an integer of at least 1; the default usually gives the best throughput. Cost is used DIUs x copy duration x the DIU-hour price (see the pricing page).
- **Lookup**: at most 5,000 rows and 4 MB of output; use it for metadata, not data. Work around it with a two-level pipeline (outer pipeline iterating over an inner one).
- **ForEach**: `batchCount` maximum 50 (default 20), at most 100,000 items, and a ForEach cannot nest inside another ForEach or an Until (use a child pipeline through Execute Pipeline).
- Incremental loads: watermark pattern (Lookup old watermark, Copy rows newer than it, then update the watermark).
- **Metadata-driven** design: one generic pipeline reading a control table instead of many near-identical pipelines.

## 4. Managed virtual network and TTL
- Time to live (TTL) applies only to a managed virtual network. You cannot enable TTL on the default auto-resolve Azure IR: create a new Azure IR for it.
- With Copy, Pipeline or External compute scale TTL active, reserved compute resources determine billing. The DIU you select for TTL is used for all copy activities and is not autoscaled, so choose enough DIUs; too few leaves activities pending in the queue. A 2-DIU setting is not supported for Copy in a managed virtual network.
- Pipeline activities run at roughly 50 per node, with Script and Lookup (SQL Always Encrypted) around 4 per node.

## Verify
- [ ] `az datafactory show` shows public network access Disabled and a system-assigned identity; every linked service uses the managed identity or Key Vault; managed private endpoints are *Approved*.
- [ ] An incremental pipeline run after inserting 10 rows copies exactly 10 and advances the watermark.

## Checked
2026-10-31. Confirmed against the Data Factory copy-activity performance features, ForEach, Lookup, integration runtime
and managed virtual network pages: DIU range 4-256 and Auto, `parallelCopies` semantics, Lookup 5,000 rows / 4 MB,
ForEach `batchCount` 50 (default 20) / 100,000 items / no nesting, IR types and self-hosted Windows-only active-active
scale-out, TTL rules, the unsupported 2-DIU managed-VNet setting and per-node activity concurrency. `az datafactory`
commands were checked against the CLI reference. Removed as unconfirmed: the `integration-runtime managed create` command,
CDC/trigger/CI-CD details (adf_publish, npm package, parameter-definition file), diagnostic table and metric names,
KQL, Stream Analytics start-mode flag, Event Grid trigger requirements and cost-driver claims.
Method: documentation only; no commands were run.
