---
id: computing-software.cloud-infrastructure-engineering.talos-linux.bare-metal-first-cluster-walkthrough
name: bare-metal-first-cluster-walkthrough
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [getting-started, bare-metal, gen-config, apply-config, bootstrap, kubeconfig, iso, maintenance-mode]
level: practitioner
status: docs-checked
description: "First Talos cluster on bare metal: boot ISO to maintenance mode, find the install disk, gen config, apply-config --insecure, set endpoints, bootstrap once, fetch kubeconfig."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/getting-started/getting-started.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every Talos cluster follows five phases: Boot, Configure, Apply, Connect, Bootstrap. Get the ISO from the Image Factory and boot it; the node shows the dashboard in **maintenance mode** (no machine config, ISO runs in RAM and touches no disk). The maintenance API is unauthenticated by design, so restrict reach with firewall rules or apply a config at boot. Unmount the ISO afterwards so you do not install onto the USB drive.

Commands from the guide, in order:

```bash
export CONTROL_PLANE_IP=<your-control-plane-ip>
talosctl get disks --insecure --nodes $CONTROL_PLANE_IP
export CLUSTER_NAME=<cluster_name>
export DISK_NAME=<control_plane_disk_name>
talosctl gen config $CLUSTER_NAME https://$CONTROL_PLANE_IP:6443 --install-disk /dev/$DISK_NAME
talosctl apply-config --insecure --nodes $CONTROL_PLANE_IP --file controlplane.yaml
talosctl --talosconfig=./talosconfig config endpoints $CONTROL_PLANE_IP
talosctl bootstrap --nodes $CONTROL_PLANE_IP --talosconfig=./talosconfig
talosctl kubeconfig --nodes $CONTROL_PLANE_IP --talosconfig=./talosconfig
talosctl --nodes $CONTROL_PLANE_IP --talosconfig=./talosconfig health
kubectl get nodes
```

`gen config` writes `controlplane.yaml`, `worker.yaml` and `talosconfig`. Workers get `worker.yaml` applied the same way, looping over a `WORKER_IP` array. Run `bootstrap` ONCE on a SINGLE control plane node. For a separate kubeconfig use `talosctl kubeconfig alternative-kubeconfig ...` and `export KUBECONFIG=./alternative-kubeconfig`. If the NIC is not detected, add network driver system extensions through the Image Factory.

## Checked

2026-11-04. Getting Started page confirms the step order, commands, maintenance-mode note and the single bootstrap warning.

Method: documentation only; no commands were run.
