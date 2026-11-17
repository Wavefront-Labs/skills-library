---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-legacy-and-zipkin-ingest
name: jaeger-legacy-and-zipkin-ingest
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, thrift-http, zipkin-compatibility, jaeger-thrift, legacy-protobuf]
level: advanced
status: docs-checked
description: "Accept legacy Jaeger Thrift and Zipkin spans: required content type, endpoints and which formats are deprecated."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
  - https://www.jaegertracing.io/docs/2.22/architecture/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep old instrumentation working during migration.

Legacy Protobuf over gRPC (collector.proto): Stable but deprecated; support was removed from OpenTelemetry SDKs and is kept for backwards compatibility.

Legacy Thrift over HTTP: Stable, Deprecated. POST a Thrift Batch struct to `/api/traces`, for example https://jaeger-collector:14268/api/traces. The Batch must use Thrift binary encoding and the request needs the header:
`Content-Type: application/vnd.apache.thrift.binary`

Legacy Thrift over UDP: Stable, Deprecated. A UDP packet containing a Thrift-encoded Batch (jaeger.thrift in the jaeger-idl repository). Most Jaeger clients use compact encoding; some libraries, notably Node.js, use binary encoding, sent to a different UDP port (compact 6831, binary 6832).

Zipkin: Stable. Jaeger accepts JSON v1/v2, Thrift and v2 Protobuf. The collector must be configured to enable the Zipkin HTTP server, for example on 9411. Two POST endpoints: `/api/v1/spans` (v1 JSON or Thrift) and `/api/v2/spans` (v2 JSON or Protobuf). The Zipkin receiver accepts v1 and v2.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 APIs page (legacy and Zipkin sections, default ports) and the Architecture page (Zipkin receiver), both read in full. Removed the closing paragraph about switching from a Zipkin backend, which neither page states.

Method: documentation only; no commands were run.
