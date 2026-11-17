---
id: computing-software.ai-ml-engineering.vllm.grpc-serving-probes
name: grpc-serving-probes
category: computing-software
field: ai-ml-engineering
product: vllm
tags: [grpc, health-checking, grpc-port, liveness, readiness]
level: advanced
status: docs-checked
description: "Serve vLLM over gRPC with --grpc and wire Kubernetes native gRPC probes to the liveness and readiness services."
sources:
  - https://docs.vllm.ai/en/latest/deployment/k8s/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace HTTP serving and httpGet probes with gRPC and health checking.

Install the optional dependencies with `pip install vllm[grpc]`, then add `--grpc` to `vllm serve` (the page example also passes `--port 50051`). The server exposes the standard gRPC Health Checking Protocol (`grpc.health.v1.Health`), which works with Kubernetes native gRPC probes (Kubernetes 1.24 or later). Replace `httpGet` probes with `grpc` probes; the page example uses `initialDelaySeconds: 120`. The health service checks engine status on each probe and returns `NOT_SERVING` if the engine is unhealthy or the server is shutting down. Manual check: `grpcurl -plaintext localhost:50051 grpc.health.v1.Health/Check`.

The Rust frontend is a separate server from `--grpc`. It starts with `VLLM_USE_RUST_FRONTEND=1 vllm serve MODEL --grpc-port 50051` or `vllm-rs serve MODEL --grpc-port 50051`, and reports liveness and readiness under separate service names:
- `liveness`: `NOT_SERVING` when the engine has failed. Pause, sleep and weight updates do not affect it.
- `readiness` and `vllm.Inference`: also `NOT_SERVING` once shutdown starts, when the engine is paused, asleep or partially awake, or a weight update has not finished successfully.
- `vllm.Control` and `""`: engine failed or shutdown started.

Point startup and liveness probes at `liveness`, readiness at `readiness`. A liveness probe on `readiness` or `vllm.Inference` restarts an engine that stays paused beyond the failure threshold.

```yaml
startupProbe:
  grpc: {port: 50051, service: liveness}
  periodSeconds: 10
  failureThreshold: 120   # allow for model loading
livenessProbe:
  grpc: {port: 50051, service: liveness}
readinessProbe:
  grpc: {port: 50051, service: readiness}
```

A paused or sleeping pod leaves its Service endpoints, so send resume, wake-up and weight-update calls to the pod directly, for example a headless Service with `publishNotReadyAddresses: true`. After a failed process checkpoint the engine stays paused and `liveness` stays `SERVING`, so whatever drives the checkpoint must restart the pod when `/checkpoint/status` reports the failure. gRPC reflection is not enabled; test with `grpc_health_probe -addr=localhost:50051 -service=readiness`. The listener stops accepting connections when shutdown starts, while `--shutdown-timeout` drains in-flight requests.

## Checked

Method: 2026-11-08 read the vLLM Kubernetes deployment page (docs source markdown) in full, concentrating on the gRPC sections.
Changes: added the plain `--grpc` health behaviour and manual grpcurl check, the liveness probe in the YAML, and the failed-checkpoint caveat. The Rust frontend service table claims were unchanged and match the page.
