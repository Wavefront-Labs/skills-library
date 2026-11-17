---
id: computing-software.cloud-infrastructure-engineering.vector.pipeline-model-and-hot-reload
name: pipeline-model-and-hot-reload
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [pipeline, dag, hot-reload, sighup, configuration, topology, vector]
level: practitioner
status: docs-checked
description: "Reason about Vector pipelines as a directed acyclic graph and reload configuration without a restart."
sources:
  - https://vector.dev/docs/architecture/pipeline-model/
  - https://vector.dev/docs/introduction/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Vector pipeline is a directed acyclic graph of components. Events flow in one direction from sources to sinks and cannot form cycles. Each component can emit zero or more events, and a configuration can contain several independent subgraphs.

Components are the generic term for sources (ingest data), transforms (parse, filter, sample, aggregate) and sinks (destinations). Each component names its upstreams with `inputs`.

Pipelines are written in YAML, TOML or JSON. YAML is the recommended default. Many users generate configuration with templating languages such as Jsonnet or CUE for maintainability. The configuration is checked at pipeline compile time, when Vector boots, which catches simple mistakes and enforces the DAG property.

In-flight changes:

- Hot reload: send `SIGHUP` to the Vector process and it applies configuration changes without restarting.
- API: a running instance can be observed and manipulated in real time through Vector's API.

```bash
kill -HUP $(pidof vector)
```

Caution: validate before reloading so a bad file does not break a working pipeline (see the validate skill). Do not add a transform whose output feeds back into its own inputs, because that forms a cycle and is rejected at startup.

Verify by editing a transform, reloading, and watching the Vector log for the reload message.

## Checked

2026-11-03. Read architecture/pipeline-model and administration/management. Confirmed: DAG with independent subgraphs, YAML/TOML/JSON with YAML recommended, Jsonnet and CUE, compile-time checks at boot, hot reload by SIGHUP, and the API. Nothing removed.

Method: documentation only; no commands were run.
