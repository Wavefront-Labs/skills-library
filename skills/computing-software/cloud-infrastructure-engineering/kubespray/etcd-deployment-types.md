---
id: computing-software.cloud-infrastructure-engineering.kubespray.etcd-deployment-types
name: etcd-deployment-types
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [etcd, deployment-type, systemd, kubeadm, docker]
level: practitioner
status: docs-checked
description: "Choose the etcd_deployment_type: host (default, systemd service), kubeadm (experimental static pod on control plane hosts, new deployments only) or docker."
sources:
  - https://kubespray.io/docs/operations/etcd.md
  - https://kubespray.io/docs/operations/upgrades.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set `etcd_deployment_type` to pick how Kubespray runs etcd. Three values are documented.

| Value | What you get |
|---|---|
| `host` | The default. etcd is installed as a systemd service. |
| `docker` | Installs docker on etcd group members and runs etcd in docker containers. Only usable when `container_manager` is `docker`. |
| `kubeadm` | Experimental, only available for new deployments. etcd runs as a static pod on the control plane hosts. |

Upgrade note from the upgrades page: `etcd_kubeadm_enabled` was deprecated at v2.19 and the same result is reached with `etcd_deployment_type: kubeadm`. From v2.19 the variable belongs in `group_vars/all/etcd.yml` rather than `group_vars/etcd.yml`, because of scope issues. If you deployed etcd with kubeadm via the old flag, remove `etcd_kubeadm_enabled`, move `etcd_deployment_type` to `group_vars/all/etcd.yml` and set it to `kubeadm`. If you never set the old flag, no change is required.

## Checked

2026-11-04. The three types and their restrictions were confirmed on the etcd page; the v2.19 migration paragraph is from the Upgrading to v2.19 section of the Upgrades page. Removed an unsupported recommendation.

Method: documentation only; no commands were run.
