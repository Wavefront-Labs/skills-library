---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.deploy-no-collector-tradeoffs
name: deploy-no-collector-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, deployment, sdk, direct-export, tradeoffs]
level: intro
status: docs-checked
description: "Weigh sending telemetry straight from SDKs to a backend against adding a Collector, and when each is enough."
sources:
  - https://opentelemetry.io/docs/collector/deploy/other/no-collector/
  - https://opentelemetry.io/docs/collector/deploy/other/agent-to-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The most direct pattern uses no Collector: applications instrumented with an OpenTelemetry SDK export traces, metrics and logs straight to a backend.

Pros:

- straightforward to use, especially in development and test environments
- no additional moving parts to deploy or operate

Cons:

- code changes are required if collection, processing or ingestion needs change
- strong coupling between application code and backend storage or visualization
- each language implementation supports only a limited number of exporters

The agent-to-gateway page lists when simpler patterns work better: applications can send telemetry directly to backends using OTLP, you do not need host-specific metrics or logs, you do not need complex processing such as tail-based sampling, or the deployment is small and operational simplicity matters more. Beyond that, an agent, a gateway or both add capabilities (centralised processing, network isolation, cost control at scale) at the price of operational complexity.

## Checked

Checked against the No Collector page and the Agent-to-gateway page (when to use, when simpler patterns work better), both read in full. Removed unconfirmed claims about CPU and memory cost in the process, host metrics being unreachable from an SDK, and the local-agent middle ground.

Method: docs-checked 2026-11-09 against the opentelemetry.io deploy/other/no-collector and deploy/other/agent-to-gateway pages (docs repo raw markdown).
