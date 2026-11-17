---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sidecar-containers-in-jobs
name: sidecar-containers-in-jobs
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, sidecar, sidecar-job-completion, native-sidecars, job, init-containers]
level: practitioner
status: docs-checked
description: "Let Jobs complete when pods carry sidecars (mesh proxies, log shippers): native sidecars via restartPolicy Always, and legacy workarounds."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/", "https://kubernetes.io/blog/2023/08/25/native-sidecar-containers/", "https://github.com/istio/istio/blob/master/pilot/pkg/features/pilot.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidecars in Jobs

## The problem
A Job completes when all pod containers terminate. A classic sidecar (Envoy, Fluent Bit,
cloud-sql-proxy) in `containers` never exits, so the Job pod runs forever after the main
container finishes.

## Native sidecars (stable in 1.33, enabled by default since 1.29)
```yaml
spec:
  template:
    spec:
      restartPolicy: Never
      initContainers:
      - name: cloud-sql-proxy
        image: <sidecar-image>
        restartPolicy: Always          # makes it a sidecar
        startupProbe:
          tcpSocket: {port: 5432}
      containers:
      - name: migrate
        image: app:1.9
        command: ["./migrate"]
```
- The kubelet starts `migrate` once the sidecar has started; with a `startupProbe`, "started" means the probe succeeded.
- When `migrate` exits, the kubelet terminates sidecars in reverse order and the pod completes.
- The sidecar does not prevent the Job from completing once the main container has finished.

## Istio
Istio's istiod reads `ENABLE_NATIVE_SIDECARS` (`true`, `false` or `auto`; default `auto`, which enables
native sidecars where supported). Ambient mode removes the sidecar altogether.

## Legacy workarounds (pre-1.29 clusters)
- The main container signals the sidecar through an application-specific shutdown endpoint, or
  writes a file to a shared emptyDir that the sidecar's wrapper watches.
- `shareProcessNamespace: true` so the main container can signal the sidecar's process.
These are fragile; upgrade instead.

## Verify
```bash
kubectl get job migrate -o jsonpath='{.status.succeeded}'
kubectl get pod -l batch.kubernetes.io/job-name=migrate -o jsonpath='{.items[0].status.phase}'   # Succeeded
```

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the sidecar containers page: an init container with `restartPolicy: Always` is a sidecar, the next init container (and app containers) start once `started` is true (process running, or startupProbe succeeded); sidecars are terminated after the main containers, in reverse order of the spec; "the sidecar container in each Pod does not prevent the Job from completing". SidecarContainers gate: beta and on by default 1.29, stable 1.33. Istio source (pilot/pkg/features/pilot.go): `ENABLE_NATIVE_SIDECARS` accepts true/false/auto, default auto.
Removed: a pinned cloud-sql-proxy image tag, the `quitquitquit` curl command (not covered by checked documentation) and the pkill claim.

Method: documentation only; no commands were run.
