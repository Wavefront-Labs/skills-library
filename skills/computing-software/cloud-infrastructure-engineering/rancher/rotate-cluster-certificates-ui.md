---
id: computing-software.cloud-infrastructure-engineering.rancher.rotate-cluster-certificates-ui
name: rotate-cluster-certificates-ui
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [certificate-rotation, rke2, kubelet, etcd, maintenance-window, webhook-certificate]
level: practitioner
status: docs-checked
description: "Rotate auto-generated certificates on Rancher-launched clusters from the UI, which services can be rotated, and why RKE2 nodes of every role go updating."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/manage-clusters/rotate-certificates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher-launched clusters generate certificates for Kubernetes components automatically. Rotate them before they expire, or if one is compromised. The page cautions that rotation can make the cluster **temporarily unavailable** while components restart, so for production use a maintenance window.

Certificates can be rotated for these services: admin, api-server, controller-manager, scheduler, rke2-controller, rke2-server, cloud-controller, etcd, auth-proxy, kubelet and kube-proxy.

Procedure:

1. **Cluster Management**, find the cluster, then the row menu **Rotate Certificates**.
2. Choose either **Rotate all Service certificates (keep the same CA)** or a single service from the dropdown.
3. Click **Save**.

The selected certificates are rotated and the related services restart to pick up the new ones.

Behaviour to expect on RKE2 (the page does not mention K3s here): etcd and control plane nodes are treated as the same server concept. Rotating a certificate for a service specific to either role therefore rotates on both, although the certificate changes only for the service you named. You will see both kinds of nodes go into an updating state, and worker-only nodes may too, because workers restart to receive the latest client certificates.

A note on the page covers people who never rotated their webhook certificates and found them expired after one year; it links a separate troubleshooting page for that case.

## Checked

2026-11-09. Read in full the Rancher Manager Certificate Rotation page (manage-clusters/rotate-certificates). Narrowed the node-behaviour note from RKE2 and K3s to RKE2, the only one the page names, and trimmed the k3s tag.

Method: documentation only; no commands were run.
