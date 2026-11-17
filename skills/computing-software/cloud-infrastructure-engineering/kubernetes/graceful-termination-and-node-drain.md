---
id: computing-software.cloud-infrastructure-engineering.kubernetes.graceful-termination-and-node-drain
name: graceful-termination-and-node-drain
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sigterm, prestop, terminationgraceperiodseconds, graceful-shutdown, endpointslices, eviction-api, poddisruptionbudget, node-drain, cordon, finalizers, stuck-terminating, force-delete, kubelet-shutdown]
level: advanced
status: docs-checked
description: "Exact ordering of pod shutdown (SIGTERM, preStop, endpoint removal), terminationGracePeriodSeconds, the eviction API vs direct delete, and debugging a pod stuck Terminating."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/", "https://kubernetes.io/docs/concepts/scheduling-eviction/api-eviction/", "https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/", "https://kubernetes.io/docs/tasks/run-application/configure-pdb/#unhealthy-pod-eviction-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Graceful termination and node drain — the shutdown path, in order

**Goal:** zero dropped requests on pod termination and a node drain that completes instead
of hanging, by knowing exactly what fires when and what blocks what.

## 1. The actual sequence on pod delete
1. Pod is marked for deletion: `metadata.deletionTimestamp` set, API server does **not**
   remove the object yet (it's now "Terminating").
2. **At the same time**: (a) the kubelet starts local shutdown: it runs any `preStop` hook,
   and only after the hook completes does it send `SIGTERM` to each container, and (b) the
   control plane evaluates removing the pod from the Service's EndpointSlices. These race — the
   endpoint is not removed instantly (terminating endpoints show `ready` false and `serving`
   still reflects readiness), and load balancers and kube-proxy may take time to reprogram. This
   is why a SIGTERM handler that exits immediately can drop in-flight requests.
3. The standard fix is a `preStop` that **sleeps** (the native `sleep` lifecycle action is stable
   since v1.34, beta and on by default from v1.30; older clusters need `exec: ["sleep", "5"]`)
   long enough for endpoint removal to propagate to kube-proxy/the mesh data plane. The sleep
   delays SIGTERM, so the grace period must cover it.
4. The grace period (`terminationGracePeriodSeconds`, default 30s) counts down from the delete
   and covers `preStop` plus normal container stop. If the hook is still running when it
   expires, the kubelet requests a one-off 2 second extension; then the runtime sends `SIGKILL`
   to anything still running.
5. Once all containers report stopped, the kubelet notifies the API server, and the pod
   object is actually removed (unless finalizers block it — see below).
- `terminationGracePeriodSeconds` must be ≥ your `preStop` sleep + actual app shutdown time,
  with headroom; sizing it too tight silently turns a graceful shutdown into a SIGKILL.

## 2. Eviction API vs plain delete
`kubectl drain` and the cluster autoscaler don't delete pods directly — they call the
**Eviction API** (`POST /pods/<name>/eviction`), which:
- Checks every PodDisruptionBudget matching the pod; if evicting would violate one, the
  call returns `429 Too Many Requests` and the caller (drain, autoscaler) retries later.
- A plain `kubectl delete pod` **bypasses PDBs entirely** — it always succeeds immediately.
  This is why an on-call "just delete the stuck pod" habit can silently blow through a
  disruption budget that `drain` would have respected.
- `unhealthyPodEvictionPolicy` on the PDB (stable since v1.31) takes `IfHealthyBudget` (the
  default) or `AlwaysAllow`; `AlwaysAllow` lets eviction proceed for running pods that are not
  Ready even if the budget is violated, so a crash-looping pod does not block drain.

## 3. Node drain mechanics
`kubectl drain <node> [--ignore-daemonsets] [--delete-emptydir-data] [--force]`:
- Cordons the node first (`unschedulable: true`) so nothing new lands there mid-drain.
- It respects PodDisruptionBudgets; if a pod's PDB can't be satisfied, drain waits on that pod —
  `kubectl get pdb` showing `ALLOWED DISRUPTIONS: 0` for the pod's budget is the diagnostic.
- `--force` continues even if there are pods that do not declare a controller;
  `--delete-emptydir-data` continues even if pods use emptyDir data.
- `--disable-eviction` makes drain use delete instead of eviction, which bypasses PDB checks.

## 4. Stuck Terminating pods
A pod stuck in `Terminating` past its grace period usually means one of:
- A **finalizer** on the pod (rare for plain pods; common on PVCs —
  `kubernetes.io/pvc-protection` — and on custom resources) is waiting for a controller to
  remove it; the object cannot be GC'd until every finalizer string is cleared.
- The kubelet on that node is unreachable (node `NotReady`) — the API server can't confirm
  the containers actually stopped, so it won't remove the object; this is a node problem,
  not a pod problem. `kubectl delete pod --grace-period=0 --force` removes the **API
  object** immediately but does **not** guarantee the container has stopped on an
  unreachable node — safe only when you've independently confirmed the node/container is
  actually gone (e.g. the node was terminated by the cloud provider).

## Gotchas
- A failing readiness probe does **not** restart the container; it only marks the pod not Ready so it
  is removed from Service endpoints. A failing liveness or startup probe restarts the container.
- Multi-container pods without sidecars: containers receive SIGTERM at different times in an
  arbitrary order — a sidecar that a main container depends on during shutdown needs its own
  coordination, or use native sidecar containers (`restartPolicy: Always` on an init container,
  stable since v1.33), which the kubelet stops after the last main container, in reverse order.
- Force-deleting a stuck pod whose container is actually still running can leave two
  instances alive briefly (old node + new scheduled pod) — dangerous for anything not
  safe to run twice (leader election, exclusive locks).

## Verify
- [ ] Load-test a rolling restart: request error rate stays ~0 with `preStop` sleep set,
      and visibly non-zero with it removed — confirms the race is real on your stack.
- [ ] `kubectl get pdb` shows `ALLOWED DISRUPTIONS >= 1` before you drain a node running
      that workload.
- [ ] A deliberately added finalizer blocks pod deletion until removed; removing it
      (`kubectl patch ... -p '{"metadata":{"finalizers":[]}}' --type=merge`) unblocks it.
- [ ] `terminationGracePeriodSeconds` comfortably exceeds measured `preStop` + shutdown time
      under load, not just at idle.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Termination flow (preStop runs before TERM, endpoint removal in parallel, default 30s grace, 2s one-off extension, SIGKILL,
  arbitrary container order, sidecar ordering): pod-lifecycle and container-lifecycle-hooks pages.
- Feature stages from the feature-gate pages: `PodLifecycleSleepAction` beta 1.30, stable 1.34; `SidecarContainers` beta 1.29,
  stable 1.33; `PDBUnhealthyPodEvictionPolicy` stable 1.31 (`IfHealthyBudget` default, `AlwaysAllow`).
- Eviction API returns 429 when a PDB blocks eviction: API-initiated eviction page.
- `kubectl drain` flags `--force`, `--ignore-daemonsets`, `--delete-emptydir-data`, `--disable-eviction` and cordon behaviour:
  kubectl `drain.go` v1.37.1 and safely-drain-node page.
- Removed: the claim that SIGTERM and preStop run in parallel, "GA 1.29" for sidecars, "beta+" for the PDB policy, the
  claim that preStop is cut off at the grace period without extension, and drain's "dependency-unaware order" remark.

Method: documentation only; no commands were run.
