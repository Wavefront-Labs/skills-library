---
id: computing-software.cloud-infrastructure-engineering.talos-linux.production-cluster-checklist
name: production-cluster-checklist
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [production, high-availability, secrets-bundle, load-balancer, system-requirements, gen-secrets, multihoming, dhcpv4config]
level: practitioner
status: docs-checked
description: "Production Talos cluster recipe: hardware minimums, TCP load balancer or DNS for the endpoint, gen secrets, versioned gen config, per-node patches, endpoints list, one bootstrap."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/getting-started/prodnotes.mdx
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/getting-started/system-requirements.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Sizing.** Minimum: control plane 2 GiB / 2 cores / 10 GiB disk, worker 1 GiB / 1 core / 10 GiB. Recommended: control plane 4 GiB / 4 cores / 100 GiB, worker 2 GiB / 2 cores / 100 GiB. Talos itself needs under 100 MB; EPHEMERAL holds images and runtime data. amd64 images need x86-64-v2; older VM CPU models (such as Proxmox `kvm64`) halt at boot.

**Endpoint.** Boot three control planes. The Talos API (TCP 50000) uses gRPC with mutual TLS, so only a TCP load balancer can front it, not an HTTP proxy. The Kubernetes endpoint is a TCP load balancer on 6443, or several A/AAAA records, e.g. `https://kube.cluster1.mydomain.com:6443`; it is also the fallback if KubePrism is down.

**Config.**

```bash
talosctl gen secrets -o secrets.yaml
talosctl gen config --with-secrets secrets.yaml $CLUSTER_NAME https://$YOUR_ENDPOINT:6443
```

Match `talosctl` to the node version; otherwise add `--talos-version`. Discover NICs and disks with `talosctl --nodes <node-ip-address> get links --insecure` and `talosctl get disks --insecure --nodes <node-ip-address>`, then patch:

```bash
talosctl machineconfig patch controlplane.yaml --patch controlplane-patch-1.yaml --output controlplane.yaml
```

Patch documents used `DHCPv4Config` plus `UnattendedInstallConfig` with `diskSelector.match: disk.dev_path == "/dev/<control-plane-disk-name>"`; prefer `disk.serial` or `disk.wwid` in production. Multihomed nodes need extra configuration (Multihoming page).

**Finish.** `talosctl config merge ./talosconfig`, `talosctl config endpoint "${CONTROL_PLANE_IP[@]}"`, then `talosctl bootstrap --nodes "$BOOTSTRAP_NODE"` once, and `talosctl kubeconfig --nodes "$BOOTSTRAP_NODE"`.

## Checked

2026-11-04. Production Clusters and System Requirements pages confirm the sizing tables, TCP-only load balancer rule and the command sequence.

Method: documentation only; no commands were run.
