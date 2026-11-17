---
id: computing-software.cloud-infrastructure-engineering.google-cloud.shielded-gke-nodes-and-secure-boot
name: shielded-gke-nodes-and-secure-boot
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, shielded-gke-nodes, secure-boot, integrity-monitoring, node-attestation, gke-hardening]
level: practitioner
status: docs-checked
description: "Use Shielded GKE nodes: verifiable node identity, enabling Secure Boot and integrity monitoring on node pools, third-party module caveats, and checking integrity failures."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/how-to/shielded-gke-nodes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shielded GKE nodes and Secure Boot

**Shielded GKE nodes** are enabled by default on Standard clusters (can be overridden) and always on in Autopilot (cannot be overridden). **Secure Boot** and **integrity monitoring** are node-pool options built on Shielded VM; Secure Boot is disabled by default on node pools.

## Commands
```bash
gcloud container clusters update prod --location=<R> --enable-shielded-nodes
gcloud container node-pools create secure-pool --cluster=prod --location=<R> \
  --shielded-secure-boot --shielded-integrity-monitoring
gcloud container clusters describe prod --location=<R>   # shieldedNodes: enabled: true
```
Disable with `--no-enable-shielded-nodes`, `--no-shielded-secure-boot` or `--no-shielded-integrity-monitoring`.

## Caveats
- On Ubuntu nodes, enabling Secure Boot blocks unsigned third-party kernel modules from loading. On Container-Optimized OS, Secure Boot does not affect kernel module loading, which is controlled separately.
- You can also monitor the integrity of the nodes' underlying Shielded VMs; see the Compute Engine integrity monitoring documentation for the log events.

Investigate unexpected integrity failures as a potential compromise: cordon, drain, and keep evidence before deleting the node.

## Verify
- [ ] The node pool configuration shows Secure Boot enabled, and `clusters describe` shows `shieldedNodes: enabled: true`.

## Checked

2026-10-24, GKE Shielded GKE Nodes how-to page on docs.cloud.google.com. Confirmed: default state on Standard and Autopilot, `--enable-shielded-nodes`, `--shielded-secure-boot`, `--shielded-integrity-monitoring` and their negations, Secure Boot disabled by default on node pools, Ubuntu versus COS behaviour for unsigned modules, the `shieldedNodes: enabled: true` describe output. Removed unconfirmed claims: node recreation on Secure Boot change, the integrity log filter, `compute.requireShieldedVm`, GKE-managed NVIDIA driver signing, Autopilot Secure Boot, baseline relearning, describe format expressions.

Method: documentation only; no commands were run.
