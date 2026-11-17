---
id: computing-software.cloud-infrastructure-engineering.kubernetes.probe-handler-types
name: probe-handler-types
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, grpc-probe, exec-probe, tcp-probe, httpget-probe, named-ports, ckad, httpheaders-probe]
level: practitioner
status: docs-checked
description: "Choose and configure probe handlers: httpGet (headers, schemes, named ports), tcpSocket, exec costs and timeouts, and native gRPC health probes."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#Probe", "https://github.com/grpc/grpc/blob/master/doc/health-checking.md"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Probe handler types

## httpGet
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: http                    # named container port; survives port changes
    scheme: HTTP                  # HTTPS is sent without verifying the certificate
    httpHeaders: [{name: Host, value: app.internal}]
```
Success = 200-399. The kubelet connects to the **pod IP** unless `host` is set; to use virtual hosts set the `Host` header in `httpHeaders` instead of `host`.
Redirects to the same host are followed; a redirect to another host counts as success and records a `ProbeWarning` event. Success depends only on the status code; the kubelet stops reading the body after 10 KiB, which can show as connection resets in the app log.

## tcpSocket
```yaml
livenessProbe:
  tcpSocket: {port: 5432}
```
Only proves something accepts TCP — a deadlocked app with an open listener passes. Fine for
databases/proxies without an HTTP endpoint; weak for app liveness.

## exec
```yaml
livenessProbe:
  exec: {command: ["pg_isready","-U","postgres","-h","127.0.0.1"]}
  timeoutSeconds: 5
```
Exit 0 = success. Each probe forks processes inside the container, which the docs warn can add CPU overhead on nodes with high pod density and short intervals; a growing number of processes can starve the container.
`timeoutSeconds` is honoured for exec probes (the `ExecProbeTimeout` gate has been on by default since 1.20). The command must exist in the image.

## grpc (GA 1.27)
```yaml
livenessProbe:
  grpc:
    port: 9090
    service: ""                   # optional name placed in the HealthCheckRequest
```
Uses the gRPC Health Checking Protocol; the app must implement it and report `SERVING`.
Plaintext by default; `mode: TLS` (no certificate verification) needs the alpha `GRPCContainerProbeTLS` gate (1.37) on kube-apiserver and kubelet. No named ports and no custom host. It replaces the older pattern of an exec probe running a separate gRPC health client.

## Choosing
| App | Readiness | Liveness |
|---|---|---|
| HTTP service | httpGet `/ready` (checks it can serve) | httpGet `/livez` (process-local only) |
| gRPC service | grpc | grpc |
| DB/queue | exec client check or tcpSocket | tcpSocket or exec with generous timeout |
| worker without port | exec checking a heartbeat file age | same |

## Verify
- [ ] `kubectl describe pod` shows the handler and no `Unhealthy` events in steady state.
- [ ] Liveness endpoint does not depend on downstream services.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the probe pages and the core/v1 Go types:
- Four mechanisms (exec, grpc, httpGet, tcpSocket); httpGet success 200-399; HTTPS probes skip certificate verification; `host` defaults to the pod IP and the docs recommend the `Host` header instead.
- Cross-host redirects count as success with a `ProbeWarning`; the response body is read only up to 10 KiB.
- gRPC probes are stable since 1.27; no named ports; plaintext default; `mode: TLS` is gated by the alpha `GRPCContainerProbeTLS` feature gate from 1.37.
- ExecProbeTimeout is stable and on by default from 1.20.
- Named ports work for HTTP and TCP probes.
Removed: the claim that gRPC probes cannot use TLS (stale since 1.37) and the "Health/Check" method path.

Method: documentation only; no commands were run.
