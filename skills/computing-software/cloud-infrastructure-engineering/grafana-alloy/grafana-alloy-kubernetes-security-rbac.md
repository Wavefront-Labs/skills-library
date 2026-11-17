---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-kubernetes-security-rbac
name: grafana-alloy-kubernetes-security-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [securitycontext, runasnonroot, readonlyrootfilesystem, rbaccreate, clusterrules, networkpolicy, uid-473]
level: advanced
status: docs-checked
description: "Harden Alloy on Kubernetes: non-root UID 473 via Helm, securityContext, eBPF capability caveats, listenAddr restriction and RBAC rules."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/access_permissions/kubernetes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy permissions on Kubernetes

The image runs as `root` by default and also defines a non-root user `alloy` with UID and GID `473`.

## Run as non-root (Helm)
```yaml
alloy:
  securityContext:
    runAsUser: 473
    runAsGroup: 473
global:
  podSecurityContext:
    fsGroup: 473
configReloader:
  securityContext:
    runAsUser: 65534
    runAsGroup: 65534
```
The config reloader sidecar runs as the `nobody` user (65534).

## Container hardening
Pod: `runAsNonRoot: true` (reject root images). Container: `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`. With a read-only root filesystem, mount a writable volume at the storage path or change `alloy.storagePath` to a mounted volume.

Caveat: `beyla.ebpf` and `pyroscope.ebpf` need root or extra Linux capabilities, so do not drop ALL when they are in the config.

## HTTP server
The chart sets `alloy.listenAddr` to `0.0.0.0` so other Pods can reach port 12345. Set it to `127.0.0.1` or add a NetworkPolicy if the UI and `/metrics` do not need cross-Pod access. The bare image defaults to `127.0.0.1:12345`. The `http` block provides TLS and authentication.

## RBAC
With `rbac.create: true` the chart makes a ClusterRole and ClusterRoleBinding from `rbac.rules` and `rbac.clusterRules`. Helm replaces arrays whole, so copy the defaults and delete blocks you do not use. Set `rbac.create: false` if you manage RBAC elsewhere. Inspect with `helm template alloy grafana/alloy --show-only templates/rbac.yaml`.

## Checked

2026-11-04. Confirmed against the Alloy access and permissions on Kubernetes page (access_permissions/kubernetes.md): UID/GID 473, Helm values, securityContext settings, eBPF caveat, listenAddr, RBAC values and helm template command. No claims changed.

Method: documentation only; no commands were run.
