---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubespray-cluster-provisioning
name: kubespray-cluster-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubespray, cluster-provisioning, ansible, kubeadm]
level: practitioner
status: docs-checked
description: "Provision and operate self-managed clusters with Kubespray: inventory, group_vars, cluster.yml, scale.yml, remove-node.yml and upgrade-cluster.yml."
sources: ["https://kubespray.io/", "https://github.com/kubernetes-sigs/kubespray/blob/master/docs/getting_started/getting-started.md", "https://github.com/kubernetes-sigs/kubespray/blob/master/docs/operations/upgrades.md", "https://github.com/kubernetes-sigs/kubespray/blob/master/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubespray provisioning

Kubespray is Ansible playbooks that wrap kubeadm, install a runtime, CNI and addons on
existing machines (bare metal or VMs).

## Setup
```bash
git clone https://github.com/kubernetes-sigs/kubespray && cd kubespray
git checkout <release-tag>                   # pin a release tag; see the README for supported versions
python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
cp -rfp inventory/sample inventory/prod
```
Check the Kubespray README for the Ansible and Python requirements of your release. A container
image (`quay.io/kubespray/kubespray:<tag>`) is an alternative to a local virtualenv.

`inventory/prod/inventory.ini` (groups as in the sample inventory):
```ini
[kube_control_plane]
cp1 ansible_host=10.0.0.11
cp2 ansible_host=10.0.0.12
cp3 ansible_host=10.0.0.13
[etcd:children]
kube_control_plane
[kube_node]
w1 ansible_host=10.0.0.21
w2 ansible_host=10.0.0.22
```
Variables live under `inventory/prod/group_vars/`: `all/all.yml` (every node),
`k8s_cluster/k8s-cluster.yml` (cluster-wide: `kube_network_plugin` with cilium, calico, kube-ovn,
flannel or cni; `kube_service_addresses`; `kube_pods_subnet`; `container_manager`, default
containerd in the sample) and `kube_control_plane.yml`. Set `kube_version` in the inventory only
if you want to pin it. Addons are in `k8s_cluster/addons.yml` (for example `metrics_server_enabled`
and `cert_manager_enabled`, both false in the sample).

## Operate
```bash
ansible-playbook -i inventory/prod/inventory.ini -b cluster.yml            # create / reconcile
ansible-playbook -i inventory/prod/inventory.ini -b scale.yml              # add worker nodes added to the inventory
ansible-playbook -i inventory/prod/inventory.ini -b remove-node.yml -e node=w2
ansible-playbook -i inventory/prod/inventory.ini -b upgrade-cluster.yml -e kube_version=<x.y.z>
```
- `scale.yml` targets the minimum needed to get kubelet installed on a new node (cluster.yml can
  also add nodes). `remove-node.yml` drains the nodes, stops services, deletes certificates and
  runs `kubectl delete node`; `-e node=a,b` selects nodes. It does not support removing the first
  control plane or etcd node; for an unreachable node add `-e '{"reset_nodes": false}'`.
- `upgrade-cluster.yml` upgrades nodes in batches of 20% of the nodes by default; set
  `-e serial=1` to go one node at a time. Pause variables exist (`upgrade_node_confirm`,
  `upgrade_node_pause_seconds`). The upgrade docs show `kube_version` without a leading `v`.

## Gotchas
- Upgrade Kubespray one release tag at a time and do not skip minor releases (patch releases are
  fine): v2.22.0 to v2.23.2 to v2.24.0 is supported, v2.22.0 straight to v2.24.0 is not.
- If you define `kube_version` in group_vars, update it or pass `-e kube_version=...`, otherwise
  the upgrade leaves the cluster at the version in your inventory.
- Keep the inventory and group_vars in Git; they are the cluster definition.
- With `kubeconfig_localhost: true` the admin kubeconfig appears under
  `inventory/<name>/artifacts/` after deployment; otherwise use `/etc/kubernetes/admin.conf` on
  control-plane nodes.

## Verify
`kubectl get nodes -o wide` shows the expected version and runtime on every node.

## Checked

Checked 2026-10-27 against Kubespray documentation (kubernetes-sigs/kubespray master: README, getting-started, upgrades and sample inventory, whose README references release v2.31.0) and Kubernetes documentation (release v1.37.1): getting-started page (cluster.yml, scale.yml, remove-node.yml with node=, first control plane or etcd node not removable, reset_nodes, kubeconfig_localhost and the artifacts directory), upgrades page (upgrade-cluster.yml, kube_version, serial default 20% batches, pause variables, do not skip minor releases and the tag example) and the sample inventory and group_vars (groups, network plugin options, container_manager, addons). Corrected the claim that upgrade-cluster upgrades one node at a time by default; replaced the pinned v2.28.0 tag and removed the ingress-nginx addon and the unconfirmed CNI warning.

Method: documentation only; no commands were run.
