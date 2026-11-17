---
id: computing-software.devops-ci-cd.deployment-strategies.rolling-update-tuning
name: rolling-update-tuning
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, rolling-update, rolling-deploy, kubernetes, k8s, maxsurge, maxunavailable, minreadyseconds, progressdeadlineseconds, readiness-probe, startup-probe, prestop, sigterm, graceful-shutdown, terminationgraceperiodseconds, poddisruptionbudget, hpa, resourcequota, statefulset-partition, daemonset, aws-ecs, minimumhealthypercent, deployment-circuit-breaker, asg-instance-refresh, rollout-duration]
level: practitioner
status: draft
description: "Tune rolling updates for speed without dropped requests: maxSurge/maxUnavailable maths, probe and minReadySeconds settings, graceful shutdown timing, quota/HPA/PDB traps, ECS and ASG equivalents."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling update tuning

**Goal:** rolling deploys that finish in a predictable time, never drop below the
capacity you need, drop zero requests, and stop themselves when the new version is bad.

(The basic rolling YAML and when to choose rolling at all are in
`computing-software.devops-ci-cd.deployment-strategies.canary-blue-green-and-rollback`.)

## 1. maxSurge / maxUnavailable arithmetic
- Percentages: `maxSurge` rounds **up**, `maxUnavailable` rounds **down**. With 3 replicas
  and the defaults 25%/25%: surge = 1, unavailable = 0 → one pod at a time.
- Batch size per step ≈ `maxSurge + maxUnavailable`. Rough rollout time:
  `ceil(replicas / batch) × (image pull + startup + readiness + minReadySeconds)`.
  40 replicas, 25%/0 → batch 10 → 4 rounds × ~60 s ≈ 4 min.
- **Capacity floor:** `maxUnavailable: 0` keeps full capacity; use it when you run
  near your limit. `maxUnavailable > 0` with `maxSurge: 0` is for when the cluster can't
  fit extra pods (no headroom) — it reduces capacity during the rollout.
- Large fleets: absolute numbers (`maxSurge: 10`) are easier to reason about than %.

## 2. Gate each batch on real readiness
- **readinessProbe** decides when a pod gets traffic and when the rollout proceeds. Make it
  reflect local ability to serve; not downstream health.
- **startupProbe** for slow starters (JVM, big models) so the liveness probe doesn't kill
  them mid-boot; don't paper over it with a huge `initialDelaySeconds`.
- **minReadySeconds** (e.g. 10-30 s): pod must stay Ready this long before counting as
  available. Catches pods that crash shortly after first passing readiness.
- **progressDeadlineSeconds** (default 600): after this with no progress the Deployment
  condition becomes `Progressing=False` — but Kubernetes does **not** roll back by itself.
  Your pipeline must act: `kubectl rollout status --timeout` → on failure
  `kubectl rollout undo`. (Argo Rollouts / ECS circuit breaker automate this.)

## 3. Zero dropped requests on the way out
Termination order: pod marked Terminating → removed from endpoints (asynchronously, via
endpoint controllers, kube-proxy, ingress controllers, cloud LBs) **and in parallel**
`preStop` runs then SIGTERM. The race means traffic can arrive after SIGTERM.
- `preStop` sleep of ~5-15 s (longer behind cloud LBs with deregistration delay) so
  routing catches up first. Newer Kubernetes supports a native `sleep` action in
  `lifecycle.preStop` (no `sleep` binary needed; *check your cluster version*).
- App handles SIGTERM: stop accepting new connections, finish in-flight, close keep-alives.
  Many frameworks need this explicitly (Node `server.close()`, Go `Shutdown(ctx)`).
- `terminationGracePeriodSeconds` > preStop + longest request drain, or SIGKILL truncates.
- PID 1 must forward signals (`exec` in entrypoint scripts, or `tini`/`dumb-init`).

## 4. Interactions that stall or break rollouts
- **ResourceQuota / cluster headroom:** surge pods that can't be scheduled leave the
  rollout Pending until the deadline. Check `kubectl describe rs` events.
- **PodDisruptionBudget** does *not* limit Deployment rolling updates (it governs
  evictions — node drains, autoscaler). Don't rely on it to slow a rollout; and a PDB of
  `maxUnavailable: 0` will block node drains forever.
- **HPA:** remove `replicas` from the Deployment manifest when an HPA owns it, or each
  apply resets the count mid-rollout. Percent-based surge scales with the HPA's current count.
- **Topology spread / anti-affinity** with `requiredDuringScheduling` can make surge pods
  unschedulable on small clusters; prefer `preferred` or ensure headroom per zone.
- `revisionHistoryLimit` too low (e.g. 0-1) removes the ReplicaSets `rollout undo` needs.

## 5. Other workload types and platforms
- **StatefulSet:** ordered, one pod at a time; use `updateStrategy.rollingUpdate.partition`
  to stage (only ordinals ≥ partition update) as a poor-man's canary. `maxUnavailable` for
  StatefulSets is newer/feature-gated in some versions (*verify*).
- **DaemonSet:** `maxUnavailable` (default 1) and `maxSurge` (cannot both be 0). For big
  clusters, 1 node at a time is very slow — use a percentage.
- **AWS ECS:** `minimumHealthyPercent: 100`, `maximumPercent: 200` ≈ surge 100%/unavailable 0;
  enable the **deployment circuit breaker with rollback**.
- **EC2 Auto Scaling instance refresh:** `MinHealthyPercentage`, warm-up, checkpoints
  (pause at % for checks), and auto-rollback options in newer APIs.

## Verify
- [ ] Measured rollout time matches the arithmetic within ~30%.
- [ ] Load test during rollout: 0 connection resets / 5xx (watch LB metrics, not only app logs).
- [ ] A build that crashes after 20 s is stopped by `minReadySeconds` + pipeline undo.
- [ ] Surge pods schedule within quota/headroom in every environment.
- [ ] `kubectl rollout history` shows enough revisions for `undo`.
