---
id: computing-software.cloud-infrastructure-engineering.kubernetes.probe-failure-debugging
name: probe-failure-debugging
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, unhealthy-event, probe-failure, liveness-probe, readiness-probe]
level: practitioner
status: docs-checked
description: "Debug failing liveness, readiness and startup probes: read Unhealthy events, reproduce the probe from inside the pod and node, and fix timing versus app bugs."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging probe failures

## Read the events
```bash
kubectl describe pod <p> | sed -n '/Events/,$p'
kubectl get events --field-selector reason=Unhealthy,involvedObject.name=<p>
```
| Message | Meaning |
|---|---|
| `HTTP probe failed with statuscode: 503` | endpoint answered, app says unhealthy |
| Event text mentioning a client timeout | no answer within `timeoutSeconds` (default 1 s; exact wording varies) |
| A dial or connection error | nothing listening on that port yet, wrong port, or the app is bound to another address |
| `Liveness probe failed: <output>` then `Killing` (`Container <name> failed liveness probe, will be restarted`) | liveness restarts |

Readiness failures only remove the pod from endpoints (READY 0/1), never restart it.

## Reproduce
Probes run from the kubelet on the node against the pod IP, not from inside the container.
```bash
kubectl get pod <p> -o jsonpath='{.status.podIP}'
# from a shell on the node (the kubelet probes from there), request the pod IP with any HTTP client
# from inside the container, use whatever HTTP client the image has against localhost
```
Works from inside but not from the node: the app is probably bound to 127.0.0.1 only. The docs say to make the endpoint listen on the pod IP address.

## Common root causes
- Slow start killed by liveness: add a startupProbe instead of a huge initialDelaySeconds.
- `timeoutSeconds` defaults to 1 s: a slow handler (GC pause, DB call) fails the probe; raise it and keep the handler cheap.
- Health endpoint checks dependencies: one DB blip restarts everything; liveness must check
  only the process.
- Named port that does not exist in the container `ports` (named ports work for httpGet and tcpSocket, not for grpc).

## Verify fix
Watch restart count and READY over a load test:
```bash
kubectl get pod <p> -w -o custom-columns=READY:.status.containerStatuses[0].ready,RESTARTS:.status.containerStatuses[0].restartCount
```

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed:
- Event message form `<Probe type> probe failed: <output>`, and the HTTP failure text `HTTP probe failed with statuscode: <code>` (kubelet source, pkg/probe/http/http.go and pkg/kubelet/prober/prober.go on master).
- The kubelet runs probes against the pod IP; httpGet success is 200-399; defaults timeoutSeconds 1, periodSeconds 10, failureThreshold 3.
- Readiness failure only marks the container not ready; liveness and startup failures kill the container.
- The liveness-exec example in the task page shows the `Unhealthy` warning followed by the `Killing` event.
Removed: exact Go timeout and exec timeout strings, the `kubectl debug node` busybox command, and claims about CNI and host firewall behaviour that no probe documentation covers.

Method: documentation only; no commands were run.
