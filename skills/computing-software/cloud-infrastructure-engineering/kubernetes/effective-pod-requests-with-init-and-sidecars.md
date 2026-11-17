---
id: computing-software.cloud-infrastructure-engineering.kubernetes.effective-pod-requests-with-init-and-sidecars
name: effective-pod-requests-with-init-and-sidecars
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, effective-requests, init-container-resources, sidecar-containers, pod-overhead, scheduling, resource-requests]
level: advanced
status: docs-checked
description: "Compute a pod's effective requests with init containers, native sidecars and pod overhead, so scheduling, quotas and autoscaler sizing match what the pod actually reserves."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/init-containers/#resource-sharing-within-containers", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/#resource-sharing-within-containers", "https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effective pod requests with init and sidecar containers

The scheduler, ResourceQuota and LimitRange use the pod's **effective** request, not just the
sum of app containers.

## Formula
For each resource:
1. Sidecars = init containers with `restartPolicy: Always` (native sidecars). They
   keep running, so they add to everything after them.
2. Effective init request = max over each init container *i* of
   `request(i) + sum(requests of sidecars started before i)`.
3. App phase request = `sum(app containers) + sum(all sidecars)`.
4. **Pod effective request = max(effective init request, app phase request) + pod overhead**
   (`RuntimeClass.overhead`, e.g. Kata/gVisor).
Limits follow the same rule. The docs state the simple form (highest init request vs sum of
non-init containers, plus pod overhead); the sidecar refinement above is the formula in the
kubernetes component-helpers `PodRequests` code, following the sidecar KEP.

## Worked example
- init `migrate`: 2 CPU
- sidecar `istio-proxy` (restartPolicy Always, declared before migrate): 100m
- app `web`: 500m, app `log-shipper`: 50m
Init phase: migrate + sidecar = 2.1. App phase: 0.5 + 0.05 + 0.1 = 0.65.
Effective = **2.1 CPU** — the pod reserves 2.1 CPU for its whole life just to run a migration.
Fix: give `migrate` a request close to the app's (it runs briefly), or move migration to a Job.

## Check what the scheduler sees
```bash
kubectl get pod p -o yaml                       # compare initContainers[*].resources with containers[*].resources
kubectl get pod p -o jsonpath='{.spec.overhead}'
```

## Implications
- ResourceQuota `requests.cpu` charges effective requests — big init containers burn quota.
- LimitRange defaults are applied to init containers too (the LimitRanger admission code loops over
  `initContainers`); an unexpectedly large default init request inflates every pod.
- Scheduling is done on effective requests, so oversized init containers reserve resources that are not
  used during the pod's life.
- Plain sidecar containers (not init containers) count only in the app phase and start only after the
  init containers finish; native sidecars start before the app containers.

## Verify
- [ ] For top workloads, effective request ≈ app-phase request (init containers not dominating).

## Checked
2026-10-23, against the Kubernetes website init containers and sidecar containers pages (effective init request/limit, pod effective request is the higher of the app-container sum and effective init request, plus pod overhead; quota and limits use effective values), the component-helpers resource source (sidecar accumulation in the init phase), and the LimitRanger admission source (init containers get defaults). The GA version number, the VPA statement and the "Allocated resources" statement were removed as unconfirmed.
Method: documentation only; no commands were run.
