---
id: computing-software.cloud-infrastructure-engineering.kubernetes.native-sidecar-startup-probe-gating
name: native-sidecar-startup-probe-gating
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, native-sidecars, sidecar-startup-probe, startup-probe, init-containers, pod-lifecycle]
level: practitioner
status: docs-checked
description: "Put a startupProbe on a native sidecar so later init containers and the app start only after the sidecar is actually ready to serve."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/", "https://kubernetes.io/docs/concepts/workloads/pods/probes/#startup-probe", "https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Startup probes on native sidecars

For a native sidecar (an init container with `restartPolicy: Always`), the kubelet moves to the
next init container, and finally the app containers, once the sidecar is *started*. Without a
startup probe, "started" means the process launched, so the app can race a proxy that is not
listening yet. With a startupProbe, the kubelet waits until it succeeds.

```yaml
spec:
  initContainers:
  - name: envoy
    image: envoyproxy/envoy:<pinned-tag>
    restartPolicy: Always
    startupProbe:
      httpGet: {path: /ready, port: 9901}   # example: your proxy's readiness endpoint
      periodSeconds: 1
      failureThreshold: 30           # up to 30 s
    readinessProbe:
      httpGet: {path: /ready, port: 9901}
  containers:
  - name: app
    image: acme/app:2.0
```

## Behaviour
- A slow `postStart` hook can delay the sidecar reaching `Running` (lifecycle hooks page).
- A sidecar's readinessProbe result is used for the Pod's `ready` state; its restart policy is `Always`, so a probe-killed sidecar is restarted on its own.
- If the startup probe never succeeds, the kubelet kills the sidecar and restarts it (restart backoff caps at 300 s); the sidecar never becomes started, so later init containers and the app containers do not start.

## Verify
```bash
kubectl get pod <p> -o jsonpath='{range .status.initContainerStatuses[*]}{.name} started={.started} ready={.ready}{"\n"}{end}'
kubectl get events --field-selector involvedObject.name=<p> | grep -i probe
```
App container `startedAt` must be later than the time the sidecar's probe first passed.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the sidecar containers page: an init container with `restartPolicy: Always` is a sidecar; the kubelet starts the next init container once the sidecar's `started` status is true, which is set when a process is running (no startup probe) or when the startupProbe succeeds; a sidecar readinessProbe determines Pod `ready`; sidecars support probes. SidecarContainers feature gate: beta 1.29, stable 1.33. Restart backoff cap of 300 s is from the pod lifecycle page.
Removed: a pinned Envoy image tag, and claims about postStart blocking order and the `Init:` status text that the documentation does not state.

Method: documentation only; no commands were run.
