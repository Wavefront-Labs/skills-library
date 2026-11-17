---
id: computing-software.cloud-infrastructure-engineering.kubernetes.container-restart-rules
name: container-restart-rules
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-lifecycle, container-restart-rules, restartpolicy, restart-policy, jobs]
level: practitioner
status: docs-checked
description: "Per-container restartPolicy and restartPolicyRules (exit-code based in-place restarts) for regular containers, and how they interact with Jobs."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-restart-rules", "https://kubernetes.io/docs/concepts/workloads/controllers/job/", "https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/5307-container-restart-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container restart rules

## Background
Historically restart behaviour was pod-level (`spec.restartPolicy`: Always, OnFailure, Never).
Native sidecars introduced container-level `restartPolicy: Always` for init containers only.

## Container-level policy and rules (alpha 1.34, beta and on by default from 1.35, gate ContainerRestartRules)
Individual containers (and regular init containers) can override the pod policy. Container `restartPolicy` accepts
`Always`, `OnFailure` or `Never`; `restartPolicyRules` can restart a container in place based on exit codes, and
requires the container `restartPolicy` to be set:
```yaml
spec:
  restartPolicy: Never          # pod-level default
  containers:
  - name: trainer
    image: trainer:1.0
    restartPolicy: Never
    restartPolicyRules:
    - action: Restart
      exitCodes:
        operator: In
        values: [42]           # retriable error code chosen by the app
```
Use case: a Job pod running an expensive workload where a known transient failure should
restart the container in place (keeping the pod, node, scheduled GPUs and emptyDir data)
instead of failing the pod and having the Job create a new one.

## Rules of thumb
- The only supported condition is `exitCodes` (operators `In` and `NotIn`) and the only supported action is `Restart`. Rules are
  evaluated in order, the first match wins, and if none match the container's own `restartPolicy` applies.
- Exit codes need a contract with the app: define which codes are retriable.
- Combine with Job `podFailurePolicy` for codes that should fail the Job immediately.
- Restarts follow the same exponential backoff as pod-level restarts.

## Without the feature
- Pod-level `OnFailure` in Jobs restarts the container in place on a non-zero exit, with backoff; those retries count
  towards `backoffLimit`.
- `podFailurePolicy` rules with `onExitCodes` and actions `FailJob`, `Ignore`, `Count` or `FailIndex` control whether the Job
  retries with a new pod.

## Verify
```bash
kubectl get pod <p> -o jsonpath='{.status.containerStatuses[0].restartCount}'
kubectl describe pod <p>          # Last State per container
```

## Checked

2026-10-26: kubernetes.io pod-lifecycle page (container restart rules section) and Job page (v1.37 docs, kubernetes/website main 2026-10-25), the ContainerRestartRules feature-gate page and KEP-5307. Confirmed: gate stages (alpha 1.34, beta default-on 1.35), restartPolicy values, restartPolicyRules requiring restartPolicy, exitCodes condition and Restart action, first-match evaluation with fallback, shared exponential backoff, Job OnFailure retries counting towards backoffLimit, podFailurePolicy actions.

Method: documentation only; no commands were run.
