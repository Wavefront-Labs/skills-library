---
id: computing-software.cloud-infrastructure-engineering.observability.jaeger-remote-sampling
name: jaeger-remote-sampling
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [jaeger-remote-sampler, remote-sampling, sampling, otel-collector, sampling-strategies]
level: advanced
status: docs-checked
description: "Centrally control head sampling with Jaeger remote sampling: collector jaeger_remote_sampling extension, strategies JSON per service/operation, and SDK jaeger_remote samplers."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/jaegerremotesampling", "https://www.jaegertracing.io/docs/latest/sampling/", "https://www.jaegertracing.io/docs/latest/apis/", "https://opentelemetry.io/docs/languages/sdk-configuration/general/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jaeger remote sampling

Remote sampling lets a central service tell SDKs which sampling rate to use per service and operation, so you change
head-sampling without redeploying. SDKs poll the endpoint and fall back to an initial rate.

## Strategies file
```json
{
  "service_strategies": [
    {"service": "checkout", "type": "probabilistic", "param": 0.5,
     "operation_strategies": [
       {"operation": "GET /healthz", "type": "probabilistic", "param": 0.0},
       {"operation": "POST /orders", "type": "probabilistic", "param": 1.0}]},
    {"service": "search", "type": "ratelimiting", "param": 100}
  ],
  "default_strategy": {"type": "probabilistic", "param": 0.05}
}
```
`ratelimiting` uses a leaky-bucket limiter at a constant rate in traces per second (for example `rate=2.0` samples 2 traces per second); the Jaeger docs say `ratelimiting` is not supported for operation strategies, so keep it at service level.
Without configuration Jaeger returns a probabilistic 0.001 (0.1%) default for all services.

## Serving it from the OTel Collector
```yaml
extensions:
  jaegerremotesampling:                 # extension id in collector-contrib
    source:
      reload_interval: 30s
      file: /etc/otel/sampling.json        # or remote: {endpoint: jaeger-collector:14250}
    http:
      endpoint: 0.0.0.0:5778
    grpc:
      endpoint: 0.0.0.0:14250
service:
  extensions: [jaegerremotesampling]
```
The extension serves the legacy HTTP endpoint (default `localhost:5778`) and a gRPC endpoint (default `localhost:14250`,
which clashes with the Jaeger receiver's port, so change one). Exactly one source, `file` (local path or
HTTP/S URL) or `remote` (a gRPC server), is allowed. Jaeger v2's own extension is named `remote_sampling` and
can also run **adaptive** sampling, which recalculates per-service/operation probabilities toward
`target_samples_per_second` and needs a `sampling_store` backend (memory, cassandra, badger, elasticsearch, opensearch).

## SDK configuration
- Standard SDK environment variables: `OTEL_TRACES_SAMPLER=parentbased_jaeger_remote` (or `jaeger_remote`) and
  `OTEL_TRACES_SAMPLER_ARG=endpoint=http://otel-agent:14250,pollingIntervalMs=5000,initialSamplingRate=0.25`
  (keys `endpoint`, `pollingIntervalMs`, `initialSamplingRate`). Support depends on the language SDK; check each SDK's docs.
Prefer the parent-based variant so downstream services honour the root decision.

## Gotchas
- Service name in the strategy must equal the SDK's `service.name` exactly.
- Head sampling cannot keep "all errors"; combine with tail sampling if you need that.

## Verify
Request the `/sampling` path on port 5778 of the collector for the service (see the Jaeger APIs page for the request form); the span rate changes within one polling interval after editing the file.

## Checked

2026-10-26, against OpenTelemetry Collector contrib jaegerremotesampling README and config.go, OpenTelemetry SDK configuration docs, and Jaeger v2.22 docs (sampling and APIs pages). Confirmed: extension id `jaegerremotesampling` and its `source` (`file`/`remote`, `reload_interval`), `http` and `grpc` blocks, default ports and the 14250 clash, strategies JSON shape, ratelimiting restriction, adaptive sampling, `parentbased_jaeger_remote`/`jaeger_remote` sampler names and argument keys. Wrong: the extension id `jaeger_remote_sampling` (it is `jaegerremotesampling`). Removed unconfirmed 60 s default polling, Java extension jar and Go API snippets, Node/Python remark and the curl query-string form.

Method: documentation only; no commands were run.
