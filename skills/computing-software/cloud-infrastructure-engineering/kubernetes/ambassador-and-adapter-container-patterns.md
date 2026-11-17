---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ambassador-and-adapter-container-patterns
name: ambassador-and-adapter-container-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, multi-container-pods, ambassador-pattern, adapter-pattern, sidecar-pattern, ckad]
level: practitioner
status: docs-checked
description: "Build ambassador (outbound proxy) and adapter (output translation) containers in one pod, with localhost wiring, ordering and when a native sidecar fits better."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers", "https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns/", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ambassador and adapter patterns

Containers in a pod share the network namespace (localhost) and can share volumes.

## Ambassador: the app talks to localhost, the ambassador talks to the world
```yaml
spec:
  initContainers:
  - name: db-proxy                          # native sidecar, starts first, stops last
    image: registry.example.com/db-proxy:<tag>   # for example a cloud database auth proxy
    args: ["--port=5432", "<instance>"]
    restartPolicy: Always
  containers:
  - name: app
    image: acme/app:1.4
    env: [{name: DB_HOST, value: "127.0.0.1"}, {name: DB_PORT, value: "5432"}]
```
Use for auth proxies, connection pooling, sharded routing, or TLS origination.

## Adapter: translate the app's output to a standard
```yaml
  containers:
  - name: legacy
    image: acme/legacy:3
    volumeMounts: [{name: status, mountPath: /var/status}]
  - name: exporter                     # reads the app's status file, serves /metrics
    image: acme/status-exporter:1.0
    ports: [{name: metrics, containerPort: 9100}]
    volumeMounts: [{name: status, mountPath: /var/status, readOnly: true}]
  volumes: [{name: status, emptyDir: {}}]
```
Common adapters: Prometheus exporters (nginx, redis, JMX), log format converters.

## Choices
- Use a native sidecar (`restartPolicy: Always` in initContainers) when the helper must be up
  before the app starts or must outlive it during shutdown (the kubelet terminates sidecars
  only after the main containers have stopped), and in Jobs (a sidecar does not stop the Job
  completing).
- Ports must not clash; all containers share the pod's network namespace.
- Give each container its own requests; the scheduler counts all of them for the pod.

## Verify
```bash
kubectl exec <pod> -c app -- wget -qO- 127.0.0.1:5432 || true
kubectl port-forward <pod> 9100 && curl -s localhost:9100/metrics | head
```

## Checked
Checked 2026-10-27 against kubernetes/website (main tree, v1.38 development; latest release
v1.37): Sidecar Containers (init containers with `restartPolicy: Always`, shared network and
storage namespaces, sidecars terminated after the main containers, Jobs complete despite a
running sidecar) and Pods (multiple containers in a pod). Replaced a pinned proxy image and
version with a placeholder.

Method: documentation only; no commands were run.
