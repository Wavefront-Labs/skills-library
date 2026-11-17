---
id: computing-software.cloud-infrastructure-engineering.keda.cluster-client-reconcile-and-grpc-tuning
name: cluster-client-reconcile-and-grpc-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [kube-api-qps, kube-api-burst, metrics-service-address, maxconcurrentreconciles, keda-scaledobject-ctrl-max-reconciles, grpc]
level: sme
status: docs-checked
description: "Tune KEDA's Kubernetes client rate limits, the gRPC metrics service address and controller concurrency for large clusters."
sources:
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flags are passed on the binary command line, while controller concurrency is set with environment variables.
Kubernetes client flags (for the Operator and Metrics Adapter binaries):
- `kube-api-qps`, default 20.0: request rate throttle toward the API server;
- `kube-api-burst`, default 30: burst allowance;
- `disable-compression`, default true: disables response compression in client-go (see the Kubernetes issue linked from the page).

gRPC metrics service: the Operator hosts a gRPC Metrics Service that serves scaling events and metrics to the Metrics API Service, which serves the Kubernetes API server. The adapter reads two flags:
- `metrics-service-address`, default `keda-operator.keda.svc.cluster.local:9666`;
- `metrics-service-grpc-authority`, default empty: a Host Authority override, needed for mutual TLS when the adapter's certificate identity differs from the address used.

Controller concurrency via environment variables on the Operator, based on controller-runtime `MaxConcurrentReconciles`:
- `KEDA_SCALEDOBJECT_CTRL_MAX_RECONCILES`, default 5, for the ScaledObjectReconciler that validates triggers, starts scaling logic and manages the HPA;
- `KEDA_SCALEDJOB_CTRL_MAX_RECONCILES`, default 1, for the ScaledJobReconciler.

The Metrics Server has its own `MetricsScaledObjectReconciler` property.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Cluster page: kube-api-qps, kube-api-burst, disable-compression, metrics-service-address and grpc-authority, the two MAX_RECONCILES variables and defaults.

Method: documentation only; no commands were run.
