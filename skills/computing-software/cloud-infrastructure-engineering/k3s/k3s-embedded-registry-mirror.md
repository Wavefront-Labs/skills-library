---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-embedded-registry-mirror
name: k3s-embedded-registry-mirror
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, spegel, embedded-registry, peer-to-peer]
level: advanced
status: docs-checked
description: "Enable the embedded Spegel distributed registry in K3s and register which upstream registries to mirror."
sources:
  - https://docs.k3s.io/installation/registry-mirror
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let nodes share container images peer to peer. It is disabled by default and needs two steps.

1. Start servers with `--embedded-registry` (or `embedded-registry: true` in config). It applies cluster-wide: every node hosts a local OCI registry on port 6443 and publishes its image list over a peer-to-peer network on port 5001. Images from airgap tarballs or pre-imports are pinned in containerd so kubelet garbage collection does not prune them. K3S_P2P_PORT can change 5001 (same on all nodes) but this is unsupported and not recommended.

2. Enable mirroring per registry in /etc/rancher/k3s/registries.yaml. The registry just needs an entry in mirrors, with or without endpoints:

```
mirrors:
  docker.io:
  registry.k8s.io:
```

A quoted "*" entry mirrors all registries. Nodes with no registry enabled do not participate at all, and only nodes with a given registry enabled exchange its images.

Requirement: all nodes must reach each other on internal IPs over TCP 5001 and 6443. Otherwise pulls are slower because the distributed registry is tried first.

Pull order with an endpoint configured: embedded mirror, then mirror.example.com, then docker.io.

The embedded registry is read-only (no docker push). Add images with `ctr -n k8s.io image pull`, or `ctr -n k8s.io image import` of a docker save archive, or the pre-import feature.

## Checked

2026-11-08. Read the full K3s Embedded Registry Mirror page (docs/installation/registry-mirror.md in the k3s-io/docs repo). Confirmed: Spegel disabled by default, --embedded-registry flag and config key, ports 6443 and 5001, pinning of air-gap and pre-imported images, K3S_P2P_PORT, the TCP reachability requirement, mirrors entries in registries.yaml, wildcard, pull order, and the read-only registry with ctr -n k8s.io. Nothing removed.

Method: documentation only; no commands were run.
