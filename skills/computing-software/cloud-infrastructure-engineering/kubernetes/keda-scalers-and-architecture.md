---
id: computing-software.cloud-infrastructure-engineering.kubernetes.keda-scalers-and-architecture
name: keda-scalers-and-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, keda, event-driven-autoscaling, scaledobject, scaledjob, scaler, triggerauthentication, cooldownperiod, queue-depth, cron, prometheus-scaler, scale-to-zero]
level: advanced
status: docs-checked
description: "KEDA's operator/metrics-server split, ScaledObject vs ScaledJob, how scalers compute metrics, and TriggerAuthentication patterns."
sources: ["https://keda.sh/docs/2.22/concepts/scaling-deployments/", "https://keda.sh/docs/2.22/concepts/scaling-jobs/", "https://keda.sh/docs/2.22/reference/scaledobject-spec/", "https://keda.sh/docs/2.22/reference/scaledjob-spec/", "https://keda.sh/docs/2.22/concepts/authentication/", "https://keda.sh/docs/2.22/operate/metrics-server/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KEDA scalers and architecture

**Goal:** know what KEDA actually runs (it's two cooperating controllers, not a single operator)
so you can debug a stuck ScaledObject instead of guessing, and pick ScaledObject vs ScaledJob
correctly.

## 1. Two components, one CRD surface
- **keda-operator** — watches `ScaledObject`/`ScaledJob` CRs, and for ScaledJobs directly creates
  Kubernetes `Job` objects when triggers fire (no HPA involved for jobs).
- **keda-operator-metrics-apiserver** — implements the `external.metrics.k8s.io` API so the
  **standard HPA controller** can query it. For `ScaledObject`, KEDA does **not** replace HPA; it
  creates a real HPA object on your behalf (`kubectl get hpa` shows a KEDA-owned HPA named after
  the ScaledObject; the default name is `keda-hpa-<scaledobject>`) and feeds it external metrics
  computed by the scalers. Do not hand-write a second HPA against the same `scaleTargetRef`; KEDA
  can take over an existing HPA only with the `scaledobject.keda.sh/transfer-hpa-ownership`
  annotation.
- Scaling is split in two phases (KEDA docs): the **activation phase** is when the KEDA operator
  decides, from each scaler's active state, whether to scale from or to zero (only 0<->1); in the
  **scaling phase** the HPA controller scales 1 to n using the metrics KEDA exposes.
  `idleReplicaCount` (must be less than `minReplicaCount`) sets the replica count used when no
  trigger is active.

## 2. ScaledObject vs ScaledJob
- **ScaledObject** — scales an existing Deployment/StatefulSet's replica count via the HPA path
  above. Use for long-running services (web, workers that poll continuously).
  - `pollingInterval` (default 30s) — how often scalers are queried.
  - `cooldownPeriod` (default 300s) — how long to wait after the last trigger reported active
    before scaling back to 0. It applies only to scaling to 0; scaling from 1 to n is handled by
    the HPA.
  - `minReplicaCount` defaults to 0 and `maxReplicaCount` to 100; `idleReplicaCount` is ignored unless set.
- **ScaledJob** — creates one Kubernetes `Job` per unit of work directly, no Deployment involved.
  Use for one-shot-per-message processing (each message = one Job pod, not a shared
  long-running consumer). `scalingStrategy.strategy` (`default`, `custom`, `accurate`, `eager`)
  controls how many Jobs to launch per polling cycle; `maxReplicaCount` (default 100) caps the
  number of Jobs. The ScaledJob reference recommends `accurate` when the scaler's `queueLength`
  does not include locked messages (Azure Storage Queue is the example).

## 3. How a scaler computes "should we scale, and by how much"
Every scaler (Kafka, SQS, RabbitMQ, Prometheus, Cron, Postgres, Azure Queue, and many more)
provides a metric value to the HPA and an active/inactive state to the KEDA operator. The HPA
applies its usual formula to the metric value and the target (for an `AverageValue` target,
`ceil(metricValue / threshold)`). Two thresholds per trigger matter and are easy to confuse:
- `threshold` — the per-replica target used in the HPA-style scaling formula (e.g. 5 messages per
  pod → 100 messages queued scales to 20 pods, capped by `maxReplicaCount`).
- `activationThreshold` — a **separate**, optional bar for the 0 <-> 1 transition (default 0, and
  activation happens only when the metric is greater than the value). Activation takes priority:
  with `threshold: 10` and `activationThreshold: 50`, 40 messages leave the scaler inactive and
  the workload at zero even though the HPA would want 4 replicas. A scaler without an
  `activation` parameter always uses 0. If `minReplicaCount` is 1 or more the scaler is always
  active and the activation value is ignored.
- Multiple triggers on one ScaledObject: the HPA evaluates all metrics and takes the one that
  needs the most replicas (`max(metrics)`).

## 4. Authentication
`TriggerAuthentication` (namespaced) or `ClusterTriggerAuthentication` (cluster-scoped) decouples
credentials from the ScaledObject: reference a Kubernetes Secret, a pod-identity/IRSA/Workload
Identity binding, or a secret provider (HashiCorp Vault, Azure Key Vault, AWS Secrets Manager,
GCP Secret Manager). A `TriggerAuthentication` can only be used by ScaledObjects in its own
namespace. Prefer pod identity over long-lived Secret-based credentials where the scaler supports it.

## Gotchas
- The HPA is generated from the ScaledObject; if autoscaling "disappeared", check for a deleted
  ScaledObject before looking at HPA config.
- `cooldownPeriod` counts from the **last time a trigger reported active**; if a trigger never
  deactivates the workload never scales to zero. Check the scaler's metric through the external
  metrics API (`kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1"` lists the exposed
  metrics), not just application logs.
- ScaledJob has no HPA to inspect; use `kubectl get scaledjob`, the operator logs and the
  `keda_scaled_job_errors_total` metric.
- By default each metric request from the HPA is routed to the KEDA Metrics Server, which queries
  the scaler; `useCachedMetrics` makes it read a cache refreshed every `pollingInterval`, which
  reduces load on the scaler service (not supported for the `cpu`, `memory` and `cron` scalers).

## Verify
- [ ] `kubectl get hpa` shows a KEDA-owned HPA per ScaledObject, and no manually created HPA
      duplicates the same `scaleTargetRef`.
- [ ] Scaling from zero happens within one `pollingInterval` of the metric exceeding
      `activationThreshold`, not only the steady-state `threshold`.
- [ ] `TriggerAuthentication` resolves without embedding a long-lived secret where pod identity is
      available.
- [ ] For ScaledJob, the number of Jobs does not exceed `maxReplicaCount` under sustained load.

## Checked

Checked 2026-10-24 against the KEDA 2.22 documentation source (kedacore/keda-docs, content/docs/2.22).
- Components, generated HPA, default HPA name `keda-hpa-<name>`, `transfer-hpa-ownership` annotation, activation vs scaling phases, activation value semantics and priority, `useCachedMetrics` and its unsupported scalers, `pollingInterval` 30s, `cooldownPeriod` 300s and its scope, `minReplicaCount` 0, `maxReplicaCount` 100, `idleReplicaCount` rule: concepts/scaling-deployments and reference/scaledobject-spec.
- ScaledJob `scalingStrategy` values (`default`, `custom`, `accurate`, `eager`), `maxReplicaCount` default 100 and when to use `accurate`: reference/scaledjob-spec. Authentication kinds and sources: concepts/authentication.
- `keda_scaled_job_errors_total`: operate Prometheus integration page.

Method: documentation only; no commands were run.
