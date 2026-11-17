---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-write-api-ports
name: jaeger-write-api-ports
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, otlp-4317, otlp-4318, zipkin-9411, collector-ports]
level: practitioner
status: docs-checked
description: "List Jaeger default ingest ports and formats: OTLP 4317/4318, Zipkin 9411, legacy Thrift 6831/6832/14268 and gRPC 14250."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
  - https://www.jaegertracing.io/docs/2.22/operations/monitoring/
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: open the right ports for senders.

Default write ports (changeable by configuration):
- 4317 gRPC: ExportTraceServiceRequest, OTLP Protobuf
- 4318 HTTP: `/v1/traces`, OTLP Protobuf or OTLP JSON
- 6831 UDP: legacy Thrift compact protocol
- 6832 UDP: legacy Thrift binary protocol
- 9411 HTTP: `/api/v1/spans` (Zipkin v1 JSON or Thrift) and `/api/v2/spans` (Zipkin v2 JSON or Protobuf)
- 14250 gRPC: `jaeger.api_v2.CollectorService`, legacy Protobuf
- 14268 HTTP: `/api/traces`, legacy Thrift

OTLP (Status: Stable) is accepted as Protobuf via gRPC, Protobuf over HTTP, and JSON over HTTP. Only tracing data is accepted, since Jaeger does not store other telemetry types.

Metrics port: the monitoring page scrapes `/metrics` on 8888 (internal telemetry port).

Failure mode: in containers, a port the collector listens on inside the container is useless unless published outside it, and a localhost bind is not reachable; the troubleshooting guide recommends 0.0.0.0 for containers.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 APIs page (default write ports table and OTLP section), the Monitoring page (8888 /metrics) and the Troubleshooting page (network connectivity), all read in full. Removed the 8889, 13133 and 27777 management ports, which none of those pages state.

Method: documentation only; no commands were run.
