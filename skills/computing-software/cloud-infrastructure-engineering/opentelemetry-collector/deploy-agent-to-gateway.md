---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.deploy-agent-to-gateway
name: deploy-agent-to-gateway
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, deployment, agent, gateway, otlp, topology]
level: practitioner
status: docs-checked
description: "Combine agent Collectors with a gateway tier so hosts export OTLP to a central Collector that owns backend credentials."
sources:
  - https://opentelemetry.io/docs/collector/deploy/other/agent-to-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Agents and gateways solve different problems, and combining them separates concerns. Agent configurations stay small, central processors handle heavier work, gateways make better sampling and batching decisions with the full picture, and gateways become a stable egress point that can handle retries and manage credentials. Agents run on each host as a DaemonSet; applications talk to local agents, agents to gateways over the internal cluster network, and gateways to backends over TLS.

Use it for centralized processing such as tail-based sampling, network isolation, or cost optimization at scale. Simpler patterns suit direct OTLP to backends, no host-specific collection, or small deployments.

Agent example: `otlp` and `host_metrics` receivers, processors `[memory_limiter, resourcedetection]`, and an `otlp` exporter to `otel-gateway:4317` with `sending_queue` `batch` using `sizer: items` and `flush_timeout: 1s`.

Guidance from the page:

- Put `memory_limiter` first in both tiers; agents need smaller limits, gateways more memory.
- Agents use smaller batches and shorter timeouts; gateways larger batches and longer timeouts.
- Run tail sampling on gateways only, with the `load_balancing` exporter in agents (`routing_key: traceID`, DNS resolver on a headless service).
- Running tail sampling across several gateways is advanced; the page prefers a single well-resourced gateway unless sticky routing is robust.
- `cumulativetodelta` also needs each series sent to one Collector.
- Probabilistic sampling across Collectors needs the same hash seed.
- Gateway credentials can come from `${env:BACKEND_API_KEY}`.

## Checked

Method: docs-checked 2026-11-09 against the opentelemetry.io deploy/other/agent-to-gateway page (docs repo raw markdown).
