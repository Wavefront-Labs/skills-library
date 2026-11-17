---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-quick-start-install-script
name: k3s-quick-start-install-script
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, install-script, get-k3s-io]
level: intro
status: docs-checked
description: "Install a single-node K3s server with the get.k3s.io install script and know what the script leaves on the host."
sources:
  - https://docs.k3s.io/quick-start
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a working single-node Kubernetes cluster with one command on a systemd or openrc host.

Run:

```
curl -sfL https://get.k3s.io | sh -
```

After the script finishes:

- The K3s service is configured to restart automatically after node reboots or if the process crashes or is killed.
- Extra utilities are installed: kubectl, crictl, ctr, k3s-killall.sh and k3s-uninstall.sh.
- A kubeconfig is written to /etc/rancher/k3s/k3s.yaml, and the installed kubectl uses it automatically.

A single-node server is a fully functional Kubernetes cluster. It contains the datastore, control-plane, kubelet and container runtime components needed to host workload pods, so adding more server or agent nodes is optional and only needed for capacity or redundancy.

Check the nodes meet the requirements page before installing. For more servers, see the high availability pages (embedded etcd or external DB).

Failure mode: each machine needs a unique hostname. If hostnames collide, pass the K3S_NODE_NAME environment variable with a valid unique hostname for each node.

## Checked

2026-11-08. Read the full K3s Quick-Start Guide (docs/quick-start.md in the k3s-io/docs repo). Confirmed: the install command, systemd or openrc scope, restart behaviour, extra utilities, kubeconfig path, single-node server being a full cluster, unique hostname requirement with K3S_NODE_NAME, and the HA page pointers. Removed the kubectl get nodes verify step (not on the page).

Method: documentation only; no commands were run.
