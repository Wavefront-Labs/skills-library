---
id: computing-software.cloud-infrastructure-engineering.kubernetes.predictive-and-scheduled-autoscaling
name: predictive-and-scheduled-autoscaling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, keda, cron-scaler, cronhpa, scheduled-scaling, predictive-scaling, minreplicas, pre-warming, traffic-shape, overprovisioning]
level: advanced
status: docs-checked
description: "Scaling ahead of known traffic shapes with cron/scheduled triggers instead of waiting for reactive HPA metrics to catch up."
sources: ["https://keda.sh/docs/2.22/scalers/cron/", "https://keda.sh/docs/2.22/reference/scaledobject-spec/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/#algorithm-details", "https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predictive and scheduled autoscaling

**Goal:** have capacity in place *before* a known traffic shape arrives, instead of letting
reactive HPA discover the spike after latency has already degraded.

## 1. Why reactive HPA is structurally late
HPA (and KEDA's ScaledObject path) can only act on a metric that has already risen — by the time
`averageUtilization` crosses the threshold, pods are already under load, and then you wait for
new pod scheduling + readiness + (if a new node is needed) node boot. For a traffic shape you *know* in advance — a 9am login surge, a nightly batch window, a
marketing push at a fixed time — that lag is avoidable, not fundamental.

## 2. Scheduled scaling mechanisms
- **KEDA Cron scaler** — a trigger type on `ScaledObject` that scales the workload to
  `desiredReplicas` between its `start` and `end` cron expressions:
  ```yaml
  triggers:
  - type: cron
    metadata:
      timezone: Australia/Sydney
      start: "0 8 * * 1-5"   # 8am weekdays: scale up window begins
      end: "0 18 * * 1-5"    # 6pm: window ends, falls back to other triggers/min
      desiredReplicas: "10"
  ```
  Combine with another trigger (CPU, queue depth) on the same ScaledObject — the HPA takes the
  metric that needs the most replicas, so `desiredReplicas` acts as a dynamic minimum during the
  window rather than an override that blocks reactive scaling above it. To be at zero outside the
  window, set `minReplicaCount: 0` on the ScaledObject; do not set `desiredReplicas: 0`.
- **CronHPA-style controllers** (community projects that manage HPA `minReplicas`/`maxReplicas` on
  a schedule) achieve the same floor-raising effect for plain HPA without KEDA — verify
  maintenance status before adopting; this space has several overlapping, less actively
  maintained projects, while KEDA's cron scaler is one of KEDA's own scalers (listed as
  community-maintained).
- **Plain scheduled `minReplicas` bump via CI/CD or a CronJob calling the Kubernetes API** — the
  lowest-tech option: a CronJob that `kubectl patch`es the HPA's `minReplicas` up 15 minutes
  before a known event and back down after. Fewer moving parts, no new CRD, but no automatic
  fallback logic if the event is cancelled/moved.

## 3. True predictive scaling (forecasting, not fixed schedule)
"Predictive" sometimes means a model forecasting load from historical patterns (e.g. day-of-week
seasonality) rather than a fixed cron. This is **not part of the HPA algorithm or the KEDA cron scaler**,
which act on a metric or a fixed schedule. Check your cloud provider's node-group documentation for
managed predictive options. Absent a managed offering, a DIY approach is: export historical
custom metrics, fit a simple model (even a weekly-seasonality rule beats nothing), write predicted
`minReplicas` values into a cron-scaler-style schedule programmatically. This is nontrivial custom
work, not a flag you flip — mark it clearly as a build project, not a quick config change.

## 4. Pairing with cluster/node autoscaling
Raising `minReplicas` ahead of time is useless if there's no node capacity to schedule those pods
— the pod-level pre-warm must be paired with either enough standing node headroom, or a
node-autoscaler-level pre-warm (e.g. scheduling a scheduled scale-up of the node group itself, or
relying on cluster/Karpenter overprovisioning pods — see the companion skill on cold-start
mitigation and overprovisioning). A cron window that starts ahead of the event gives CA/
Karpenter time to provision nodes before the real traffic arrives.

## Gotchas
- KEDA cron scaler's `start`/`end` are interpreted in the trigger's own `timezone` field, which
  must be a value from the IANA Time Zone Database (for example `Australia/Sydney`); `start` and
  `end` must not be the same expression.
- With `minReplicaCount: 0`, scale-down to zero happens `cooldownPeriod` (default 300s) after the
  cron `end`, so replicas stay up for a while past the window.
- The cron scaler scales within the window; it does not scale on a recurring schedule outside it,
  and `useCachedMetrics` is not supported for it.
- Over-scheduling "just in case" (wide windows, generous `desiredReplicas`) defeats the cost
  benefit of autoscaling at all — size the window and floor to the actual known event, not a
  comfortable guess, and revisit with real traffic data after the first few occurrences.

## Verify
- [ ] A dry run of the cron window (`kubectl get hpa -w` across the start/end boundary) shows
      the replica count rising before the known traffic event and falling back after,
      without flapping at the boundary.
- [ ] Node capacity (via CA/Karpenter) is confirmed available by the time the pod-level floor
      rises — not racing a cold node boot during the real event.
- [ ] Timezone is an IANA zone name.
- [ ] The schedule is documented next to the known business event it serves (a launch calendar,
      a batch job schedule) so it gets updated when that event's timing changes.

## Checked

Checked 2026-10-24 against the KEDA 2.22 documentation source (scalers/cron.md, reference/scaledobject-spec.md) and the HPA page of Kubernetes v1.37 documentation (kubernetes/website main, the latest published release on 2026-10-24).
- Cron trigger fields (`timezone` from the IANA database, `start`, `end`, `desiredReplicas`), the YAML example shape, "start and end must not differ... not be the same", `desiredReplicas` acting as a dynamic minimum because the HPA takes the max across metrics, the `minReplicaCount: 0` pattern, cooldown 5 minutes after `end`, community maintainer and `useCachedMetrics` exclusion: KEDA cron scaler page.
- HPA takes the largest desired replica count across metrics: HPA page.

Method: documentation only; no commands were run.
