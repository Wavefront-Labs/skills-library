---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-additional-control-plane-upgrade
name: kubeadm-additional-control-plane-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cluster-upgrade, additional-control-plane-upgrade, kubeadm-upgrade-node, kubeadm-upgrade, certificate-renewal-flag]
level: practitioner
status: docs-checked
description: "Upgrade the second and third control-plane nodes with kubeadm upgrade node after the first one, including drain, kubelet upgrade and etcd checks."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Upgrading additional control-plane nodes

`kubeadm upgrade apply` runs once, on the first control plane. Every other control-plane node
uses `kubeadm upgrade node`, which fetches the `ClusterConfiguration` from the cluster, upgrades
the node's control-plane static pod manifests and the kubelet configuration, and renews the
certificates kubeadm manages (optionally backing up the kube-apiserver certificate).

## Per node, one at a time
```bash
# 1. kubeadm binary (Debian/Ubuntu with pkgs.k8s.io repo for the target minor)
sudo apt-mark unhold kubeadm && sudo apt-get update && sudo apt-get install -y kubeadm='<target>.x-*' && sudo apt-mark hold kubeadm
kubeadm version

# 2. upgrade the control-plane components on this node
sudo kubeadm upgrade node

# 3. drain, upgrade kubelet/kubectl, restart
kubectl drain cp2 --ignore-daemonsets
sudo apt-mark unhold kubelet kubectl && sudo apt-get install -y kubelet='<target>.x-*' kubectl='<target>.x-*' && sudo apt-mark hold kubelet kubectl
sudo systemctl daemon-reload && sudo systemctl restart kubelet
kubectl uncordon cp2
```

## Between nodes, check
```bash
kubectl get pods -n kube-system -o wide | grep cp2         # new static pods Running
kubectl -n kube-system get pod kube-apiserver-cp2 -o jsonpath='{.spec.containers[0].image}'
etcdctl ... endpoint health --cluster                        # all members healthy before the next node
```
Never take down the next node while the previous etcd member is still catching up; with three
members you can lose only one at a time.

## Notes
- `kubeadm upgrade node` writes backups to `/etc/kubernetes/tmp/kubeadm-backup-manifests-*` and
  `kubeadm-backup-etcd-*`; keep them until the upgrade is verified.
- Certificates are renewed by default; pass `--certificate-renewal=false` only if you manage
  certs externally.
- kubeadm rolls a failed component upgrade back automatically; if that does not work, the
  `kubeadm-backup-manifests-*` folder (and `kubeadm-backup-etcd-*` for local etcd) can be restored
  by hand. The `/etc/kubernetes/tmp` backups must be removed manually afterwards.
- The same command on workers only updates the kubelet config.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25). Confirmed: `upgrade apply` runs on the first control-plane node only and `upgrade node` on additional ones; what `upgrade node` does on control-plane and worker nodes; the `/etc/kubernetes/tmp/kubeadm-backup-etcd-*` and `kubeadm-backup-manifests-*` folders; certificate renewal default and `--certificate-renewal=false`; drain before a minor kubelet upgrade. Removed as unconfirmed: the pinned package version and the "safe to re-run" claim.

Method: documentation only; no commands were run.
