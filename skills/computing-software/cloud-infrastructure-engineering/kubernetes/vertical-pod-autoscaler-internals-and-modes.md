---
id: computing-software.cloud-infrastructure-engineering.kubernetes.vertical-pod-autoscaler-internals-and-modes
name: vertical-pod-autoscaler-internals-and-modes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, vpa, vertical-pod-autoscaler, recommender, updater, admission-controller, resource-requests, in-place-resize, inplacepodverticalscaling, oomkilled, right-sizing, histogram, vpa-off-mode, resourcepolicy, minallowed, vpa-hpa-conflict]
level: advanced
status: docs-checked
description: "VPA's three components, its three update modes, how the recommender builds its histogram, and when in-place resize replaces evict-and-recreate."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/components.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/api.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/features.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/known-limitations.md", "https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/flags.md", "https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# VPA internals and update modes

**Goal:** set CPU/memory requests from observed usage instead of guessing, without the
evict-storms and recommendation lag that make teams distrust VPA.

## 1. The three components
VPA is not one controller — it is three, each watching the same `VerticalPodAutoscaler`
object:
- **Recommender** — builds an in-memory model seeded from `VerticalPodAutoscalerCheckpoint`
  objects (or Prometheus), adds fresh samples from the Metrics API, and writes
  `status.recommendation` (lowerBound, target, upperBound, uncappedTarget) onto the VPA object.
  It does not touch pods.
- **Updater** — compares live pod requests to the recommendation; if they differ significantly
  (the threshold comes from the recommended min and max values) it **evicts** the pod through the
  Eviction API, which respects PodDisruptionBudgets, so the replacement picks up new requests via
  the admission controller. It can instead perform an in-place update when an in-place mode is
  used. This is why VPA without in-place resize causes restarts.
- **Admission controller** — a mutating webhook that intercepts pod creation and patches
  container resources to the current recommendation. It only fires on create, not on running pods —
  that's the updater's job to force via eviction.

If any one component is missing from your install (common when people only deploy the
recommender for "recommendations only"), the others' behaviour silently doesn't happen —
check that the `vpa-recommender`, `vpa-updater` and `vpa-admission-controller` Deployments
are running (`kubectl get deploy -n kube-system`) before assuming a mode works.

## 2. Update modes (`spec.updatePolicy.updateMode`)
- **`"Off"`** — recommender only. Read `status.recommendation` and apply manually, or feed it
  into CI as a PR that bumps `resources.requests`. Zero risk, zero automation. Default choice
  for stateful or latency-sensitive workloads until you trust the numbers.
- **`"Initial"`** — admission controller sets requests on pod creation only; no evictions ever.
  Good for workloads with natural churn (frequent deploys, HPA-driven scale events) where you
  get fresh sizing without extra disruption.
- **`"Recreate"`** — the API default. The updater evicts pods whose requests drift too far
  from the recommendation; the recreated pod gets fresh resources via the admission controller.
  This is "classic VPA" and the one that surprises people with restarts during business hours —
  it has no awareness of traffic patterns, only of the recommendation threshold.
- **`"InPlaceOrRecreate"`** — tries an in-place resize first and falls back to `Recreate`.
- **`"InPlace"`** — in-place updates only, never evicts (needs the VPA `InPlace` feature gate).
- **`"Auto"`** — deprecated; the API reference says it is currently equivalent to `Recreate`
  and will be removed in a future API version. Don't use it in new manifests.

## 3. In-place resize (KEP-1287)
Kubernetes lets CPU/memory requests and limits change **without** recreating the pod, gated by
`InPlacePodVerticalScaling` (alpha 1.27, beta and on by default 1.33, stable 1.35).
- `resizePolicy` per container chooses `NotRequired` (default) or `RestartContainer` per
  resource; the Kubernetes docs say memory changes often need `RestartContainer` because many
  runtimes cannot adjust memory dynamically, and that a memory limit decrease is only a
  best-effort attempt to avoid OOM kills when the policy is `NotRequired`.
- VPA drives this through `InPlaceOrRecreate` (alpha in VPA 1.4.0, beta and on by default from
  1.5.0, gate removed in 1.7.0) and the eviction-free `InPlace` mode (alpha in VPA 1.7.0). `Recreate`
  still evicts. Even in-place updates cannot be guaranteed disruption-free.

## 4. The histogram and why recommendations lag
- Historical samples lose weight over time: `--cpu-histogram-decay-half-life` and
  `--memory-histogram-decay-half-life` both default to 24h. History is stored in
  `VerticalPodAutoscalerCheckpoint` objects by default (or read from Prometheus), so
  recommendations survive recommender restarts.
- A freshly created VPA has little history, so its recommendation is less reliable at first and a
  rare weekly spike will not be reflected until it has been observed. Start in `Off` mode and
  read the recommendation before switching to `Recreate`.
- After an OOM kill the memory recommendation is bumped by `--oom-bump-up-ratio` (default 1.2) or
  at least `--oom-min-bump-up-bytes` (default 100Mi).

## 5. VPA + HPA
The VPA known-limitations doc says VPA should not be used with HPA on the same resource metric
(CPU or memory); VPA on memory with HPA on CPU, or HPA on custom and external metrics, is fine.
A common pairing: VPA for request sizing, HPA on a custom/external metric (RPS, queue depth)
for replica count. See
`computing-software.cloud-infrastructure-engineering.kubernetes.horizontal-pod-autoscaling-and-upgrade-strategy`.

## Gotchas
- The updater does not evict when a workload has fewer live replicas than `--min-replicas`
  (default 2) or `updatePolicy.minReplicas`; a PDB can also block eviction.
- `containerPolicies` with `minAllowed`/`maxAllowed` bound the recommendations — without them a
  noisy-neighbour spike can recommend very large requests that then get applied.
- Recommendations are **per-container**, not per-pod; a sidecar with its own tiny footprint gets
  its own histogram and can be starved if you only read the main container's number.
- VPA has no knowledge of HPA's target utilization — if HPA targets 65% CPU and VPA resizes
  requests upward, the *absolute* CPU threshold to trigger scale-out moves too; re-check HPA
  behavior after a VPA-driven resize settles.

## Verify
- [ ] `kubectl describe vpa <name>` shows non-empty `target`/`lowerBound`/`upperBound` after
      letting it observe for a while.
- [ ] The three VPA Deployments are running in `kube-system`.
- [ ] A deliberately undersized pod gets evicted (Recreate) or resized without restart (in-place,
      if enabled and confirmed) within a few updater cycles (`--updater-interval` default 1m).
- [ ] HPA and VPA are not targeting the same metric on the same workload.

## Checked

Checked 2026-10-24 against the kubernetes/autoscaler vertical-pod-autoscaler docs (master, VPA 1.8.1) and Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- Component roles, checkpoint/Prometheus history, Metrics API samples, PDB-respecting eviction: components.md.
- `updateMode` enum and meanings (default `Recreate`; `Auto` deprecated and currently equivalent to `Recreate`; `InPlaceOrRecreate`, `InPlace`): api.md.
- In-place stages and requirements: features.md; `InPlacePodVerticalScaling` stages (alpha 1.27, beta 1.33, stable 1.35): feature gate source; `resizePolicy` values and memory-decrease behaviour: Kubernetes resize page.
- Decay half-lives, OOM bump flags, `--min-replicas`, `--updater-interval`: flags.md. VPA with HPA: known-limitations.md.

Method: documentation only; no commands were run.
