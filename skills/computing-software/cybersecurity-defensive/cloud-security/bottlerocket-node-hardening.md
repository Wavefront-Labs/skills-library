---
id: computing-software.cybersecurity-defensive.cloud-security.bottlerocket-node-hardening
name: bottlerocket-node-hardening
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [bottlerocket, container-optimized-os, immutable-os, eks-nodes, selinux, node-hardening, cloud-workload-protection]
level: practitioner
status: draft
description: "Run Kubernetes nodes on Bottlerocket: immutable read-only root, SELinux enforcing, API-driven settings, admin container off, update operator and CIS checks."
sources: ["https://bottlerocket.dev/en/os/latest/", "https://github.com/bottlerocket-os/bottlerocket/blob/develop/SECURITY_FEATURES.md", "https://github.com/bottlerocket-os/bottlerocket-update-operator", "https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami-bottlerocket.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bottlerocket node hardening

Bottlerocket is a minimal, container-host Linux: no package manager, no SSH by default, read-only
dm-verity root filesystem, SELinux enforcing, atomic A/B updates.

## Security properties
- **Immutable root** with dm-verity: tampering with OS files is detected (boot fails) - attackers cannot persist in the OS.
- **SELinux enforcing** with policy that confines containers (even privileged ones have restrictions on host files).
- Minimal attack surface: no shell in the host by default; access via **control container** (SSM) and optional **admin container**.
- Kernel lockdown (integrity mode) and secure boot support on supported platforms.

## Configuration (user data TOML / API settings)
```toml
[settings.host-containers.admin]
enabled = false          # keep off; enable temporarily for debugging only
[settings.host-containers.control]
enabled = true           # SSM access - disable if not needed
[settings.kernel]
lockdown = "integrity"
[settings.kubernetes]
cluster-name = "prod"
```
Changes at runtime with `apiclient set ...` from the control container (audited via SSM).

## Updates
Image-based A/B updates: Bottlerocket Update Operator (Brupop) on Kubernetes, or managed node groups /
Karpenter AMI updates (replace nodes). Track variant releases for CVE fixes.

## Compliance
Built-in CIS Bottlerocket benchmark and Kubernetes worker node checks: `apiclient report cis` and
`apiclient report cis-k8s` (from the admin/control container).

## Gotchas
- Debugging habits (SSH in, install tools) do not work; use ephemeral debug containers and the admin container sparingly with logging.
- Some agents (legacy EDR expecting packages/kernel modules) are unsupported; use DaemonSet/eBPF-based agents that support Bottlerocket.

## Verify
- [ ] Admin container disabled across node groups.
- [ ] `apiclient report cis` passes level 1 on a sample node.
- [ ] Nodes on a Bottlerocket version without open critical CVEs.
