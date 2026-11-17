---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-reset-and-node-rejoin
name: kubeadm-reset-and-node-rejoin
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, kubeadm-reset, node-rejoin, kubeadm-join, cni-cleanup, iptables-flush, etcd-member-remove, node-cleanup]
level: practitioner
status: docs-checked
description: "Cleanly tear a node out of a kubeadm cluster with kubeadm reset, scrub what reset leaves behind (CNI, iptables, etcd membership), and re-join it without ghost state."
sources: ["https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-reset/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-token/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm reset and node re-join

**Goal:** remove a node (worker or control plane) from a kubeadm cluster and bring it back
in a known-clean state. `kubeadm reset` does less than people assume — the leftovers are
what cause the second join to fail.

## 1. Drain and delete the node from the API first
```bash
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
kubectl delete node <node>
```
Delete the Node object so the cluster no longer lists the node; the node then re-registers
cleanly on re-join.

## 2. Control-plane node — remove its etcd member BEFORE reset
For control-plane nodes `kubeadm reset` also removes this node's local stacked etcd member from
the etcd cluster. If the reset cannot reach the cluster (for example the node is already dead),
remove the member yourself from a healthy control-plane node and confirm with `member list`:
```bash
kubectl -n kube-system exec etcd-<healthy> -- etcdctl \
  --endpoints=https://127.0.0.1:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key \
  member list -w table
# ... member remove <hex-id>
```
With an external etcd, `kubeadm reset` does not delete any etcd data; wipe it with etcdctl
if a new cluster will reuse the same endpoints.

## 3. Run reset on the node
```bash
sudo kubeadm reset -f            # add --cri-socket unix:///run/containerd/containerd.sock if it can't detect
```
`kubeadm reset` is a best-effort revert: it cleans the node's local files created by `kubeadm
init` or `kubeadm join`. It does **not** clean (per the reset reference):
```bash
sudo rm -rf /etc/cni/net.d                  # CNI config; a different CNI's leftovers can conflict on the next join
sudo rm -rf $HOME/.kube/config              # the kubectl credential copied from admin.conf
```
It also leaves iptables, nftables and IPVS rules alone (kube-proxy's control loop keeps them
in sync); the docs say leaving them should not cause issues if the host is reused as a node or
for something else. To clean them, run the cluster's own kube-proxy image with
`kube-proxy --cleanup`.

## 4. Re-join
```bash
# on a control plane: mint a fresh token (the token from init has a 24h TTL)
kubeadm token create --print-join-command
# control-plane re-join needs certs re-uploaded (the certificate key expires after 2 hours)
kubeadm init phase upload-certs --upload-certs   # prints a new certificate-key
```
Then run the printed `kubeadm join ... [--control-plane --certificate-key <key>]` on the node.

## Gotchas
- `kubeadm reset` does not uninstall packages or the container runtime.
- Kubelet drop-in settings such as `--node-ip` in `KUBELET_EXTRA_ARGS` are not part of what
  reset reverts; check they are still right before the re-join.
- CNI plugins use `/etc/cni/net.d` by default; if your CNI is configured elsewhere, clean that
  path instead.

## Verify
- [ ] `kubectl get nodes` shows the node `Ready` with the expected version and no stale labels/taints.
- [ ] A test pod scheduled on it (`nodeName`) gets an IP in the current pod CIDR and can reach CoreDNS.
- [ ] Control plane: `etcdctl member list` shows exactly one entry for this host, status started.

## Checked

Checked 2026-10-26 against Kubernetes documentation v1.37 (kubernetes/website and kubernetes/kubernetes master, commit dates 2026-10-24/25) (`kubeadm-reset.md`, `kubeadm-token.md`, `kubeadm-init.md`). Confirmed: reset is a best-effort revert and removes the local stacked etcd member on control-plane nodes; it leaves external etcd data, `/etc/cni/net.d`, iptables/nftables/IPVS rules and `$HOME/.kube` untouched and documents the `kube-proxy --cleanup` approach; the 24 hour token TTL and 2 hour certificate-key lifetime. Removed as unconfirmed: the claim that reset silently skips the etcd member when the API server is unhealthy, the exact list of directories reset wipes, the CNI-specific leftover interface names, the Node-object CSR failure explanation and the reboot advice. Also corrected: `kubeadm reset` documentation says leftover iptables and IPVS rules are normally harmless.

Method: documentation only; no commands were run.
