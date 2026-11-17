---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-remote-sampling-endpoints
name: jaeger-remote-sampling-endpoints
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, remote-sampling-api, port-5778, port-5779, sampling-manager]
level: practitioner
status: docs-checked
description: "Know the remote sampling endpoints, port 5778 HTTP /sampling and 5779 gRPC, and check them with curl."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
  - https://www.jaegertracing.io/docs/2.22/operations/troubleshooting/
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: verify that SDKs can fetch sampling strategies.

Remote sampling APIs (status stable):
- 5778, HTTP, `/sampling`, sampling.proto via Protobuf-to-JSON mapping.
- 5779, gRPC, `jaeger.api_v2.SamplingManager`, Protobuf.

The `remote_sampling` extension runs the HTTP/gRPC servers that expose this API; the API follows the protocol defined in sampling.proto.

Verify what the server returns for a service (the troubleshooting guide's example):
`curl "jaeger-collector:14268/api/sampling?service=foobar"`
which returns something like `{"strategyType":"PROBABILISTIC","probabilisticSampling":{"samplingRate":0.001}}`.

If remote sampling seems broken:
1. Confirm the SDK is actually configured to use remote sampling, points to the correct sampling service address, and that the address is reachable from the application's network namespace.
2. Confirm the server returns the strategy you expect for the service.

Some but not all OpenTelemetry SDKs support remote sampling, often via extensions.

To rule out sampling when spans are missing, set the SDK to sample everything; OpenTelemetry SDKs default to `parentbased_always_on`, changeable via `OTEL_TRACES_SAMPLER`. Enabling the SDK's stdout exporter shows whether spans are recorded at all.

## Checked

2026-11-08: confirmed against the Jaeger 2.22 APIs page (remote sampling ports), the Troubleshooting page (curl example, SDK defaults, stdout exporter) and the Configuration page (remote_sampling extension), all read in full.

Method: documentation only; no commands were run.
