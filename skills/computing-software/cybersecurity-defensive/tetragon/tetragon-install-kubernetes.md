---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-install-kubernetes
name: tetragon-install-kubernetes
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [install-k8s]
level: practitioner
status: docs-checked
description: "Install, configure, upgrade and uninstall Tetragon on a Kubernetes cluster with the Helm 3 chart from helm.cilium.io."
sources:
  - "https://tetragon.io/docs/installation/kubernetes/"
  - "https://tetragon.io/docs/reference/helm-chart/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Tetragon on Kubernetes with Helm

Goal: run the Tetragon agent as a daemonset on a cluster. Helm 3 with the chart from the `helm.cilium.io` repository is the recommended method.

## Install

```shell
helm repo add cilium https://helm.cilium.io
helm repo update
helm install tetragon cilium/tetragon -n kube-system
kubectl rollout status -n kube-system ds/tetragon -w
```

Any chart value can be overridden with `--set KEY1=VALUE1,KEY2=VALUE2`. By default, pods in the kube-system namespace are filtered out of events. If Tetragon fails to start because of BTF issues, see the BTF question in the Tetragon FAQ.

## Kind clusters

The Helm value `tetragon.hostProcPath` (default `/proc`) is the location of the host proc filesystem. Environments like kind, where the runtime itself does not run on the host, are an exception, so set it there. The Helm chart reference describes the value.

## Configure

Change values with `helm upgrade`:

```shell
helm upgrade tetragon cilium/tetragon -n kube-system --set tetragon.grpc.address=unix:///var/run/tetragon/custom-tetragon.sock
```

Alternatively edit the `tetragon-config` ConfigMap and restart the daemonset:

```shell
kubectl edit cm tetragon-config -n kube-system
kubectl rollout restart ds/tetragon -n kube-system
```

Talos Linux (v1.12.0+) requires this Helm values entry:

```yaml
extraHostPathMounts:
  - name: sys-kernel-tracing
    mountPath: /sys/kernel/tracing
```

## Upgrade and uninstall

```shell
helm upgrade tetragon cilium/tetragon -n kube-system --version 0.9.0
helm uninstall tetragon -n kube-system
```

## Checked

Date: 2026-11-07

Kubernetes page read in full. The kind cluster YAML and the /procHost mount are not on that page, so they were removed; the kind remark now rests on the Helm chart reference hostProcPath description (page read in full, added to sources).

Method: documentation only; no commands were run.
