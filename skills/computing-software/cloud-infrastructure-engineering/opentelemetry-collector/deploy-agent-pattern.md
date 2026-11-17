---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.deploy-agent-pattern
name: deploy-agent-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, deployment, agent, daemonset, sidecar]
level: practitioner
status: docs-checked
description: "Run the Collector as an agent next to workloads, as a host process, DaemonSet or sidecar, to offload and enrich telemetry."
sources:
  - https://opentelemetry.io/docs/collector/deploy/agent/
  - https://opentelemetry.io/docs/collector/deploy/other/agent-to-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the agent pattern, telemetry comes from applications instrumented with an OpenTelemetry SDK that exports over OTLP, or from Collectors using the OTLP exporter. It goes to a Collector instance that runs alongside the application or on the same host, such as a sidecar or a DaemonSet. The Collector then sends it to one or more backends.

Each SDK or downstream Collector is configured with the address of a Collector instance, for example:

```shell
export OTEL_EXPORTER_OTLP_ENDPOINT=http://collector.example.com:4318
```

A minimal trace pipeline on that Collector receives OTLP over HTTP on `0.0.0.0:4318`, exports with the `otlp` exporter (the page names the exporter `otlp/jaeger`, pointing at a Jaeger OTLP endpoint) with `sending_queue` set to `batch:`, and wires them in a `traces` pipeline.

Pros: straightforward to start, and a clear one-to-one mapping between application and Collector. Cons: limited scalability for teams and infrastructure resources, and inflexible for complex or evolving deployments.

When agents feed a gateway tier, keep agent configuration small and focused and let central processors do heavier work. Put `memory_limiter` first in the pipeline (agents typically need smaller limits than gateways), use smaller batches and shorter timeouts than the gateway, and configure `sending_queue` on the exporter to absorb short gateway outages. The agent-to-gateway page's examples bind to `0.0.0.0` for convenience; the Collector defaults to `localhost`, which is preferable when all clients are local.

## Checked

Checked against the Agent deployment pattern page (example, trade-offs) and the Agent-to-gateway page (agent guidance, memory limiter, batching, sending queue, endpoint binding warning), both read in full. Removed unconfirmed claims about host-level data reachability, local enrichment benefits and per-node resource cost, which neither page states.

Method: docs-checked 2026-11-09 against the opentelemetry.io deploy/agent and deploy/other/agent-to-gateway pages (docs repo raw markdown).
