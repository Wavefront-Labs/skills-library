---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.deploy-gateway-pattern
name: deploy-gateway-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, deployment, gateway, load-balancer, central]
level: practitioner
status: docs-checked
description: "Run Collectors as a central gateway that receives from agents and applications, applies shared processing and exports to backends."
sources:
  - https://opentelemetry.io/docs/collector/deploy/gateway/
  - https://opentelemetry.io/docs/collector/deploy/other/agent-to-gateway/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In the gateway pattern, applications or other Collectors send OTLP to a single endpoint provided by one or more Collector instances running as a standalone service, for example a Kubernetes deployment. Typically there is one endpoint per cluster, data centre or region.

Single tier: an out-of-the-box load balancer (the page shows NGINX with `grpc_pass` on port 4317 and `proxy_pass` on 4318 over three upstream Collectors) distributes load. The load balancer is external to the Collectors.

Two tiers: when telemetry must be processed in a specific Collector, the first-tier Collector uses the load-balancing exporter and the second tier receives data directed to it. Example: first tier routes so that all spans of a trace reach the same second-tier Collector running the tail sampling processor.

Load-balancing exporter fields:

- `resolver`: `static` with `hostnames`, or `dns` with `hostname` (and optional `port`), which re-resolves periodically.
- `routing_key`: `traceID` exports spans by trace ID; `service` exports by service name, useful with the span metrics connector so one downstream Collector sees all spans of a service.

The exporter emits metrics including `otelcol_loadbalancer_num_backends` and `otelcol_loadbalancer_backend_latency` to monitor the Collector serving the OTLP endpoint.

Pros: separation of concerns such as centrally managed credentials, and central policy management (for example filtering logs or sampling). Cons: one more thing to maintain and that can fail, added latency with cascaded Collectors, higher overall resource use.

Scaling: gateways scale vertically and horizontally. Without tail sampling any load balancer or Kubernetes service with round-robin distribution works and instances operate independently; with tail sampling, agents must route by trace ID. Put `memory_limiter` first in the pipeline and use larger batches and longer timeouts than agents.

Single writer: every OTLP metric stream needs a single writer with a globally unique identity. Multiple writers of the same series cause gaps, jumps or backend errors such as `Error on ingesting out-of-order samples` on Prometheus. Use the Kubernetes attributes processor and resource detection processor to give resources distinct identity.

## Checked

Checked against the Gateway deployment pattern page and the Agent-to-gateway page (scaling and processing sections), both read in full. Removed unconfirmed claims about fewer vendor connections, the minimum of two instances and aggregation needing series-affine routing in general.

Method: docs-checked 2026-11-09 against the opentelemetry.io deploy/gateway and deploy/other/agent-to-gateway pages (docs repo raw markdown).
