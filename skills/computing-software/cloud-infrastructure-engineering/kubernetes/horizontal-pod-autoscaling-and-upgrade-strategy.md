---
id: computing-software.cloud-infrastructure-engineering.kubernetes.horizontal-pod-autoscaling-and-upgrade-strategy
name: horizontal-pod-autoscaling-and-upgrade-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, hpa, horizontalpodautoscaler, autoscaling-v2, metrics-server, custom-metrics, external-metrics, prometheus-adapter, keda, scale-to-zero, behavior, stabilizationwindowseconds, vpa, vertical-pod-autoscaler, canary, blue-green, progressive-delivery, argo-rollouts, flagger, analysis, rollback, surge-capacity, scaling-policies, averageutilization]
level: advanced
status: docs-checked
description: "Scale and ship Kubernetes workloads together: HPA v2 metrics and behavior, KEDA, HPA/VPA conflicts, and choosing rolling, blue-green or canary with automated analysis."
sources: ["https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/", "https://keda.sh/docs/latest/concepts/scaling-deployments/", "https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler", "https://argo-rollouts.readthedocs.io/en/stable/features/canary/", "https://rollouts-plugin-trafficrouter-gatewayapi.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HPA and upgrade strategy — scaling with load and releasing without regret

**Goal:** replica count follows demand without flapping, and new versions reach users in a
way that limits blast radius and rolls back on metrics, not on someone noticing. Basic
rolling-update fields (`maxSurge`, `maxUnavailable`, `rollout undo`) are in
`computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes`.

## 1. HPA v2 essentials
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata: {name: api}
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: api}
  minReplicas: 3
  maxReplicas: 30
  metrics:
  - type: Resource
    resource: {name: cpu, target: {type: Utilization, averageUtilization: 65}}
  - type: Pods
    pods: {metric: {name: http_requests_per_second}, target: {type: AverageValue, averageValue: "50"}}
  behavior:
    scaleUp:   {stabilizationWindowSeconds: 0,   policies: [{type: Percent, value: 100, periodSeconds: 30}]}
    scaleDown: {stabilizationWindowSeconds: 300, policies: [{type: Pods,    value: 2,   periodSeconds: 60}]}
```
- Formula: `desired = ceil(current × currentMetric / target)`; with several metrics the
  **largest** result wins. A 10% tolerance (the default, set cluster-wide by
  `--horizontal-pod-autoscaler-tolerance`) suppresses tiny changes; a per-HPA `tolerance` field
  under `behavior.scaleUp` / `behavior.scaleDown` is stable from Kubernetes 1.37 (`HPAConfigurableTolerance`).
- `Utilization` is a percentage of the **request**, not the limit or the node. If a container
  has no request for the resource, utilisation is undefined and the HPA takes no action for that
  metric.
- Pods that are not Ready, or still starting, are treated conservatively (see
  `--horizontal-pod-autoscaler-initial-readiness-delay`, default 30s, and
  `--horizontal-pod-autoscaler-cpu-initialization-period`, default 5 minutes); a long startup
  makes scale-up feel slow.
- Remove `replicas` from the Deployment manifest in Git once HPA owns it.

## 2. Pick the right signal
- **CPU** works for CPU-bound stateless services. Memory is a poor scaling signal: most
  runtimes do not release memory when load falls, so it scales up and never down.
- **Requests per second / in-flight requests** via Prometheus Adapter (custom metrics API)
  tracks user load more directly.
- **Queue depth / lag** (Kafka, SQS, RabbitMQ) via **KEDA**, which also scales to zero.
  KEDA creates and owns the HPA — do not define a second HPA on the same target. KEDA handles
  the 0<->1 activation itself and the generated HPA handles 1<->N. Plain HPA can also scale to
  zero (`minReplicas: 0`) for object or external metrics only, never CPU or memory: the
  `HPAScaleToZero` gate is beta and on by default from Kubernetes 1.37 (alpha since 1.16), and it
  must be enabled on both kube-apiserver and kube-controller-manager.
- Choose a target utilisation that leaves headroom for the time new pods (and maybe new nodes)
  take to arrive. The right number depends on your startup and autoscaler latency; measure.

## 3. HPA and VPA
- Never let HPA and VPA both act on CPU/memory of the same workload; they fight.
- Common safe combo: VPA in `updateMode: "Off"` (recommendations only) to set requests,
  HPA on CPU or a custom metric for count. VPA update modes are `Off`, `Initial`, `Recreate`,
  `InPlaceOrRecreate` and `InPlace`; `Auto` is deprecated since VPA 1.4.0 (alias of `Recreate`).
  In-place pod resize (`InPlacePodVerticalScaling`) is stable from Kubernetes 1.35 (beta from
  1.33); `InPlace` mode needs 1.33+ and the VPA `InPlace` feature gate on the updater and
  admission controller.

## 4. Choosing an upgrade strategy
| Strategy | Cost | Rollback | Use when |
|---|---|---|---|
| Rolling (`maxUnavailable: 0`) | ~+25% pods briefly | redeploy old ReplicaSet, minutes | most stateless services, backward-compatible changes |
| Recreate | downtime | redeploy | singleton that must not run two versions |
| Blue-green | 2× capacity during switch | flip Service selector, seconds | risky releases, need instant rollback, schema already compatible |
| Canary | small extra | shift weight back, seconds | high traffic, metrics good enough to judge a 5% slice |

- Every strategy except Recreate runs **two versions at once**: DB migrations must be
  expand/contract (add columns first, remove later) and APIs backward-compatible.
- During a rollout with `maxSurge: 25%` at 30 replicas you briefly run about 38 pods — check
  quota and node headroom.

## 5. Progressive delivery with analysis
Argo Rollouts replaces the Deployment strategy with steps and metric gates:
```yaml
strategy:
  canary:
    canaryService: api-canary
    stableService: api-stable
    trafficRouting: {plugins: {argoproj-labs/gatewayAPI: {httpRoute: api, namespace: shop}}}
    steps:
    - setWeight: 5
    - analysis: {templates: [{templateName: error-rate}]}
    - setWeight: 25
    - pause: {duration: 10m}
    - setWeight: 100
```
- The `AnalysisTemplate` queries Prometheus (e.g. 5xx ratio < 1% and p99 latency) and
  aborts → automatic rollback on failure.
- Without a traffic router, canary weight is approximated by replica ratio — 1 of 10 pods
  = 10%, not 5%.
- Plugin names and field shapes for Gateway API routing differ by Argo Rollouts version;
  copy from the docs for yours.

## Gotchas
- `scaleDown` stabilization defaults to 300 s; shortening it causes flapping on spiky load.
- `minReplicas: 1` + a PDB with `minAvailable: 1` blocks node drains.
- If the metrics API is unavailable the HPA cannot compute a desired count and stops scaling —
  alert on HPA status conditions (`kubectl describe hpa`) or you silently stop scaling.
- Cold JIT/caches: new pods are slow for the first minute, so a canary judged in its first
  60 s looks worse than it is — pause before analysis.
- Cluster (control plane/node) version upgrades are a separate procedure not covered here.

## Verify
- [ ] `kubectl get hpa` shows real metric values, not `<unknown>`.
- [ ] Load test: replicas rise within the expected window and fall after load stops without oscillation.
- [ ] Quota and node headroom cover `maxReplicas` + surge.
- [ ] A deliberately broken canary is aborted and rolled back by analysis with no human action.
- [ ] Migrations for the release are backward-compatible with the previous version.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; v1.37 latest release) HPA concept page, feature-gate stage pages, VPA concept page and kube-controller-manager reference; Argo Rollouts canary and analysis docs (master) and the Argo Rollouts Gateway API plugin quick start (main). Confirmed: autoscaling/v2 behaviour block, largest-of-metrics rule, 10% default tolerance, 300 s default downscale stabilisation, utilisation relative to requests, HPAScaleToZero beta default-on in 1.37 for object and external metrics, InPlacePodVerticalScaling stable in 1.35, VPA update modes and `Auto` deprecation, Rollouts plugin key `argoproj-labs/gatewayAPI` with `httpRoute` and `namespace`, replica-ratio canary weight without a traffic router. Fixed: the claim that scale-to-zero needs KEDA (native HPA scale-to-zero is now beta). Removed as unconfirmed: the 60-70% target and 30-90 s startup figures, the surge-pods-in-average statement and the FailedGetResourceMetric reason name.

Method: documentation only; no commands were run.
