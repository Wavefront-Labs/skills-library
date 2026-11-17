---
id: computing-software.cloud-infrastructure-engineering.jaeger.jaeger-adaptive-sampling
name: jaeger-adaptive-sampling
category: computing-software
field: cloud-infrastructure-engineering
product: jaeger
tags: [jaeger, adaptive-sampling, sampling-store, target-samples-per-second, initial-sampling-probability]
level: advanced
status: docs-checked
description: "Enable adaptive sampling so Jaeger recalculates per-service and per-endpoint probabilities toward a throughput target."
sources:
  - https://www.jaegertracing.io/docs/2.22/architecture/sampling/
  - https://www.jaegertracing.io/docs/2.22/deployment/configuration/
  - https://www.jaegertracing.io/docs/2.22/architecture/apis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let the backend tune sampling to traffic.

Adaptive sampling observes received spans and recalculates the probability for each service/endpoint combination so the volume of collected traces matches `target_samples_per_second`. A newly detected service or endpoint is sampled with `initial_sampling_probability` until enough data exists to compute a suitable rate.

Configure it in the `remote_sampling` extension instead of a file:
```
remote_sampling:
  adaptive:
    sampling_store: some_store
    initial_sampling_probability: 0.1
  http:
  grpc:
```
Use either `file` or `adaptive` in `remote_sampling`.

It also needs the `adaptive_sampling` processor in the pipeline, which observes all traces collected by Jaeger and calculates the probabilities for the throughput targets.

Storage: adaptive sampling needs a `sampling_store` backend to keep observed traffic and computed probabilities. Supported sampling storage: memory (for all-in-one), cassandra, badger, elasticsearch and opensearch. The docs link a sample configuration and a blog post on the engine.

Compared with the file-based approach, adaptive sampling needs no hand-edited strategies per service: the strategies are generated from observed traffic. The default Remote Sampling API ports are 5778 (HTTP, `/sampling`) and 5779 (gRPC, `jaeger.api_v2.SamplingManager`).

## Checked

Method: docs-checked 2026-11-09 against the Jaeger 2.22 sampling, configuration and APIs pages (read in full).
