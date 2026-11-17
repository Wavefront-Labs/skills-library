---
id: computing-software.cloud-infrastructure-engineering.kubernetes.container-lifecycle-hooks
name: container-lifecycle-hooks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, lifecycle-hooks, poststart, prestop, sleep-action, graceful-shutdown, ckad]
level: practitioner
status: docs-checked
description: "Use postStart and preStop hooks correctly: exec/httpGet/sleep handlers, how they interact with terminationGracePeriodSeconds, and the failure modes that hang or kill containers."
sources: ["https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/", "https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container lifecycle hooks (postStart, preStop)

## postStart
Runs right after the container is created, **asynchronously with** the entrypoint — no
guarantee it runs before the app starts. The container is not `Running` until postStart
returns; if the hook fails the container is killed (and restarted per restartPolicy).
Use for: tiny registration steps. Do not use for: waiting for dependencies (use init
containers) or long work (a slow hook can keep the container from reaching `Running`).

## preStop
Runs when termination starts, **before** SIGTERM is sent. The grace period clock
(`terminationGracePeriodSeconds`, default 30s) covers preStop **plus** the app's SIGTERM
handling. If preStop takes 25s of a 30s budget, the app gets 5s before SIGKILL.
```yaml
spec:
  terminationGracePeriodSeconds: 45
  containers:
  - name: web
    lifecycle:
      preStop:
        sleep: {seconds: 10}          # sleep action: beta 1.30, stable 1.34; no shell needed
      # exec: {command: ["/bin/sh","-c","sleep 10"]}   # older clusters, needs a shell
      # httpGet: {path: /drain, port: 8080}
```
Why the classic `sleep`: endpoint removal (EndpointSlice update → kube-proxy/ingress/LB) is
asynchronous with SIGTERM. A short sleep keeps serving while load balancers stop sending new
connections, which reduces errors during rollouts.

## Handler types
- `exec` — runs inside the container; the command must exist in the image.
- `httpGet` — kubelet calls the container; app can drain itself.
- `sleep` — kubelet-side pause (alpha 1.29, beta 1.30, stable 1.34); a zero value is allowed by default from 1.33.
- `tcpSocket` is deprecated for hooks and not honoured.

## Debugging
```bash
kubectl describe pod p
kubectl get events --field-selector reason=FailedPreStopHook
```
The logs of a hook handler are not exposed in Pod events; a failed handler only emits the event.

## Gotchas
- preStop is called when a container is terminated by an API request or a management event such as a liveness or startup probe failure, preemption or resource contention. The call fails if the container is already terminated or completed.
- Delivery is at least once, so a hook can run more than once; make hooks idempotent. If either hook fails, the container is killed.

## Verify
- [ ] A rollout under load shows zero 5xx; preStop + drain fits inside the grace period.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the lifecycle hooks page: postStart runs concurrently with the entrypoint and can delay the container reaching Running; preStop must finish before TERM is sent and the grace period starts before it runs, covering hook plus shutdown; handlers are exec, HTTP and sleep (tcpSocket deprecated and unsupported); a failed hook kills the container; delivery is at least once; FailedPostStartHook and FailedPreStopHook events. Feature gates: PodLifecycleSleepAction beta 1.30, stable 1.34; PodLifecycleSleepActionAllowZero beta 1.33, stable 1.34.
Removed: the claim that preStop never runs on crashes or OOM kills beyond the documented "fails if already terminated", the /proc/1/fd/1 logging trick, and numeric sleep suggestions.

Method: documentation only; no commands were run.
