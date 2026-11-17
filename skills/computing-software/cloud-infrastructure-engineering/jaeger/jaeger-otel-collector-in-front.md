---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-otel-collector-in-front
name: jaeger-otel-collector-in-front
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, opentelemetry-collector, sidecar, host-agent, remote-sampling-proxy]
level: practitioner
status: docs-checked
description: "Decide whether to place an OpenTelemetry Collector sidecar, agent or remote cluster in front of Jaeger."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: weigh optional collector tiers.

Jaeger v2 is itself a customized distribution of the OpenTelemetry Collector, so you do not need a separate OTel Collector. If you already use one for other telemetry or for pre-processing and enriching traces, place it in front of Jaeger. It can run as an application sidecar, a host agent/daemon, or a remote service cluster. It supports Jaeger's Remote Sampling protocol and can serve static configurations from files or proxy requests to the Jaeger backend (for example with adaptive sampling).

As sidecar or host agent:
- Benefits: SDK trace export and sampling endpoints can both point at a local host, with no remote discovery; the collector can enrich data (for example with the k8s pod name); enrichment cost is spread across hosts.
- Downside: an extra layer of marshaling and unmarshaling.

As a remote cluster:
- Benefit: sharding capabilities, for example with tail-based sampling.
- Downside: the same extra marshaling layer.

The agent role of Jaeger itself is discouraged in favor of the standard OpenTelemetry Collector.

## Checked

2026-11-08: read the whole Architecture page (raw markdown from the jaegertracing/documentation repo, v2/2.22). Confirmed the three placements, the benefits and downsides, the Remote Sampling support and the agent-role recommendation.

Method: documentation only; no commands were run.
