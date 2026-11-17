---
id: computing-software.cloud-infrastructure-engineering.cilium.policy-entities-reference
name: policy-entities-reference
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, entities, toentities, fromentities, world, kube-apiserver]
level: advanced
status: docs-checked
description: "Reference of Cilium policy entities (host, remote-node, kube-apiserver, ingress, cluster, cluster-mesh, init, health, world, all) with gotchas."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Entities

Use `fromEntities` and `toEntities`. Defined entities:
- `host`: local host including host-network containers on it.
- `remote-node`: any node in connected clusters except the local host (incl. host-network containers).
- `kube-apiserver`: the API server, in-cluster or external.
- `ingress`: the Cilium Envoy that handles ingress L7; also applies to pod-to-pod hairpinning via ingress.
- `cluster`: all endpoints in the local cluster incl. unmanaged endpoints, host, remote-node, init, ingress, health, kube-apiserver and remote nodes in clustermesh.
- `cluster-mesh`: all endpoints in meshed clusters plus `cluster`.
- `init`: endpoints without a resolved identity (bootstrap phase), typically non-Kubernetes.
- `health`: the per-node health endpoints.
- `unmanaged`: endpoints not managed by Cilium; part of `cluster`.
- `world`: everything outside the cluster; allowing to world equals allowing CIDR 0.0.0.0/0.
- `all`: all known clusters plus world, whitelists everything.

## Gotchas
- `kube-apiserver` may not work for ingress traffic on AKS and GKE because control-plane ingress is tunneled through worker nodes and loses the source IP; try `fromEntities: cluster`. Egress `toEntities: kube-apiserver` is expected to work.
- Kubernetes automatically allows communication from the local host to local endpoints; run the agent with `--allow-localhost=policy` to control it via policy.

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the Layer 3 policy page (entities section and notes): https://docs.cilium.io/en/stable/security/policy/layer3/. Confirmed the entity definitions, the AKS and GKE kube-apiserver note and the allow-localhost note stated above. Nothing was removed.

Method: documentation only; no commands were run.
