---
id: computing-software.cloud-infrastructure-engineering.kubernetes.restart-backoff-and-restartpolicy-semantics
name: restart-backoff-and-restartpolicy-semantics
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, restartpolicy, crashloopbackoff, exponential-backoff, container-restart, kubelet, restart-count, backoff-reset, job-restartpolicy, liveness-probe-restart, container-vs-pod-restart]
level: practitioner
status: docs-checked
description: "The kubelet's container restart backoff behind CrashLoopBackOff timing, and how restartPolicy Always/OnFailure/Never changes who restarts what."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-restarts", "https://kubernetes.io/docs/concepts/workloads/controllers/job/#handling-pod-and-container-failures", "https://github.com/kubernetes/kubernetes/blob/master/pkg/features/kube_features.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restart backoff and restartPolicy semantics: who retries what, and how fast

**Goal:** know what controls the delay between restarts and which layer (kubelet vs controller)
does the retrying. Symptom-based OOM and exit-code debugging is in
`computing-software.cloud-infrastructure-engineering.kubernetes.troubleshooting-crashloops-and-oom`;
this is the restart-timing mechanism underneath it.

## 1. The kubelet's per-container backoff
The Pod `restartPolicy` only governs restarts that make replacement containers **inside the same
Pod, on the same node**, handled by the kubelet. After containers exit, the kubelet restarts
them with an exponential backoff delay (10s, 20s, 40s, ...) capped at 300 seconds (5 minutes).
Once a container has executed for 10 minutes without problems, the kubelet resets the backoff
timer for that container. `CrashLoopBackOff` appears in the Status column of some kubectl
output while the backoff is in effect; Status is a kubectl display field, not the Pod `phase`.

Tuning (check the stage for your release):
- `KubeletCrashLoopBackOffMax`: alpha in 1.32, beta and on by default from 1.35. Set
  `crashLoopBackOff.maxContainerRestartPeriod` (between `"1s"` and `"300s"`) in the
  KubeletConfiguration to change the cap per node; delays still start at 10s and double, and if
  the value is under 10s the initial delay becomes that value.
- `ReduceDefaultCrashLoopBackOffDecay`: alpha since 1.33 (off by default); start at 1s and cap at
  60s cluster-wide. A per-node setting takes precedence over it.

## 2. restartPolicy: who creates the replacement
`spec.restartPolicy` is `Always` (default), `OnFailure` or `Never`. It applies to app containers
and regular init containers; native sidecars ignore it (see
`computing-software.cloud-infrastructure-engineering.kubernetes.init-containers-and-sidecar-lifecycle`).

| Exit | Always | OnFailure | Never |
|---|---|---|---|
| 0 | restarts | does not restart | does not restart |
| non-zero | restarts | restarts | does not restart |

- Deployments allow only `Always`; Jobs commonly use `OnFailure` or `Never`.
- If the whole Pod fails (node lost, kicked off the node, or a container fails under `Never`),
  the controller (ReplicaSet, Job) creates a new Pod. For a Job, each pod failure counts toward
  `.spec.backoffLimit` (default 6); the Job controller recreates failed Pods with its own
  exponential delay (10s, 20s, 40s ...) capped at ten minutes. With `OnFailure`, the container
  re-runs locally in the same Pod and the in-place retries across containers also count toward
  `backoffLimit`.
- Since Kubernetes 1.35 (beta, `ContainerRestartRules` on by default; alpha in 1.34), individual
  containers can set their own `restartPolicy` and `restartPolicyRules` to override the Pod
  policy. Individual-container restarts follow the same backoff.

## Gotchas
- Containers in one pod have separate restart timers, but the Pod stays not Ready while any
  container is not ready.
- Deleting a Pod gives its replacement fresh state, so the backoff starts over at the short
  end; the underlying cause is untouched.
- Check logs of the previous run with `kubectl logs <pod> -c <container> --previous`.

## Verify
- [ ] Crash a test container and confirm consecutive restart delays roughly double up to 300s.
- [ ] A container running cleanly for 10 minutes restarts the next failure at the short delay.
- [ ] For a Job with `restartPolicy: Never`, each retry shows as a new pod name.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Pod Lifecycle" (container restarts, restart
behaviour table, restart delay features) and "Jobs" (handling failures, backoff failure policy),
plus feature-gate stages from `kube_features.go` on main (v1.38 development; latest release
v1.37.1). Confirmed: 10s doubling to 300s, 10-minute reset, Pod versus kubectl Status, restart
table, Job backoffLimit semantics, gate stages above. Removed unconfirmed claims: restartCount
never resets, liveness restarts sharing the timer, kubelet restart clearing timers, etcd
persistence statements, and the "only Never" Job claim (OnFailure Jobs also count retries).
Method: documentation only; no commands were run.
