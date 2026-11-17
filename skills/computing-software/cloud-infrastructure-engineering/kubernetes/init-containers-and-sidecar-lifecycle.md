---
id: computing-software.cloud-infrastructure-engineering.kubernetes.init-containers-and-sidecar-lifecycle
name: init-containers-and-sidecar-lifecycle
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, init-containers, sidecar, native-sidecars, restartpolicy-always, container-startup-order, pod-phase, probe-order, istio-proxy, envoy-sidecar, ambient-mesh, shutdown-order]
level: advanced
status: docs-checked
description: "Init container ordering and retry semantics, native sidecars (initContainers with restartPolicy: Always; GA 1.33), and startup/shutdown ordering."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/init-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Init containers and sidecar lifecycle: ordering and native sidecars

**Goal:** get startup and shutdown ordering right for pods that need setup work before the
main container, or a companion process alongside it.

## 1. Init containers: sequential, retried until they succeed
- `spec.initContainers` run **one at a time, in list order**; each must succeed before the next
  starts, and app containers start (in parallel) only after all have completed. The Pod is
  `Pending` with condition `Initialized` false and cannot be Ready until then.
- If an init container fails, the kubelet restarts it according to the Pod `restartPolicy`; with
  Pod policy `Always`, init containers use `OnFailure`, so they are retried until they succeed.
  With `Never`, a failed init container makes the whole Pod fail. Read `kubectl describe pod`
  events for the failing init container, not the app container.
- Resource accounting: the effective init request/limit is the highest across init containers;
  the Pod's effective request/limit is the higher of that and the sum of the non-init (app and
  sidecar) containers, plus pod overhead. Scheduling uses these effective values, so a heavy
  one-shot init container can require a larger node than steady state.
- Regular init containers do not support `lifecycle`, `livenessProbe`, `readinessProbe` or
  `startupProbe`, but support resource limits, volumes and their own `securityContext`.
- If the Pod restarts, all init containers run again.

## 2. Native sidecar containers
A native sidecar is an entry in **`initContainers`** with container-level `restartPolicy: Always`
(the `SidecarContainers` gate: beta and on by default since v1.29, GA in v1.33):
```yaml
initContainers:
- name: proxy
  image: <proxy-image>
  restartPolicy: Always
  # optional startupProbe / readinessProbe
containers:
- name: app
  image: <app-image>
```
- It starts in init order and keeps running for the Pod's life. The kubelet starts the **next**
  init container (and eventually the app containers) once the sidecar's `started` status is
  true: when a process is running and there is no startup probe, or when its `startupProbe`
  succeeds. So a `startupProbe` is the way to hold the app back until the sidecar is up.
- Sidecars support probes; a `readinessProbe` on one contributes to the Pod's Ready state.
- Sidecars ignore the Pod-level `restartPolicy`; they always restart.
- On termination the kubelet postpones stopping sidecars until the main container has fully
  stopped, then stops them in reverse order of their position in the spec. This avoids the old
  proxy-dies-first race.
- Their SIGTERM and SIGKILL may arrive without time to exit gracefully if other containers use
  the whole grace period, so non-zero sidecar exit codes at termination are normal and should
  be ignored by external tooling.
- In a Job, a sidecar does not prevent the Job from completing after the main container ends.
- Changing a sidecar's image restarts that container, not the Pod.
- Sidecar requests and limits are summed with app containers in the effective Pod value, and the
  Pod's effective QoS tier counts init, sidecar and app containers alike.

## 3. Older clusters and mixed approaches
Before native sidecars (or if an injector does not use them), sidecars were ordinary entries in
`containers`; Kubernetes does not control which starts or stops first among those. The docs say
this is still appropriate when you do not need to control ordering, or must support Kubernetes
versions without container-level `restartPolicy`. Ordering workarounds (a `postStart` wait loop,
a `preStop` coordination step) are application-specific; confirm behaviour for your mesh version.

## Gotchas
- An init container that never exits blocks the Pod in `Init` indefinitely; `activeDeadlineSeconds`
  can bound it, but it also applies after the Pod is running, so use it mainly for Job-style Pods.
- Only the `image` field of an init container can be updated on an existing Pod, and doing so
  does not restart the Pod.

## Verify
- [ ] `kubectl describe pod` shows each regular init container `Terminated: Completed` with exit
      code 0, in declared order, before any app container starts.
- [ ] A native sidecar is stopped after the main container on termination (check exit times).
- [ ] A heavy one-shot init container's request does not force unexpectedly large node sizing.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Init Containers", "Sidecar Containers" and
"Pod Lifecycle" (current docs), and the Kubernetes 1.33 release notes (latest release v1.37.1).
Confirmed: sequential init semantics and retry rule, sidecars defined in `initContainers`,
start-order condition (`started`, startup probe), termination order, probe support, Job note,
resource rules, SidecarContainers beta 1.29 and GA 1.33. The 1.33 notes say the gate was locked
to its default and slated for removal in v1.36. Removed the unconfirmed ambient-mesh remarks and logging-agent
backoffLimit remark.
Method: documentation only; no commands were run.
