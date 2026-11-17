---
id: computing-software.cloud-infrastructure-engineering.kubernetes.replacing-a-failed-control-plane-node
name: replacing-a-failed-control-plane-node
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, control-plane-node-replacement, failed-control-plane-node, etcd-member-remove, stacked-etcd, quorum, control-plane-ha, node-replacement, disaster-recovery]
level: advanced
status: docs-checked
description: "Runbook for a dead control-plane node in a stacked-etcd kubeadm cluster: remove the stale etcd member first, delete the Node, then join a replacement with --control-plane."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/high-availability/", "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/", "https://etcd.io/docs/v3.5/faq/", "https://kubernetes.io/docs/setup/best-practices/certificates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replacing a failed control-plane node

**Goal:** a control-plane VM is gone (disk died, cloud terminated it). The cluster still
works on 2/3 quorum, but you are one failure from an outage. Replace it without ever dropping
below quorum.

## 1. Confirm what you have
```bash
kubectl get nodes -l node-role.kubernetes.io/control-plane
ETCD="kubectl -n kube-system exec etcd-<alive-node> -- etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt --key=/etc/kubernetes/pki/etcd/healthcheck-client.key"
$ETCD member list -w table
$ETCD endpoint status --cluster -w table     # the dead one errors; note which has IS LEADER=true
```
If only one member is reachable you are **below quorum** - stop, this is the
`etcd-cluster-membership-and-recovery` path (restore from snapshot with `--force-new-cluster`).

## 2. Remove the dead etcd member FIRST
Order matters: adding the new member before removing the old one makes a 4-member cluster
that needs 3 for quorum - and you only have 2 alive.
```bash
$ETCD member remove <hex-id-of-dead-member>
$ETCD member list -w table                   # now 2 members, both started
```

## 3. Remove the Node object and any stale kube-vip/keepalived state
```bash
kubectl delete node <dead-node>
```
If the dead node held the API VIP (kube-vip leader, keepalived MASTER), confirm the VIP moved:
`ping <vip>` / `curl -k https://<vip>:6443/readyz` from a worker.

## 4. Join the replacement
On a surviving control plane:
```bash
kubeadm init phase upload-certs --upload-certs       # new certificate-key
kubeadm token create --print-join-command --certificate-key <key>
```
On the new machine (same OS prep: containerd, kubelet/kubeadm packages, swap off, sysctls):
```bash
kubeadm join <controlPlaneEndpoint>:6443 --token ... --discovery-token-ca-cert-hash sha256:... \
  --control-plane --certificate-key <key> --apiserver-advertise-address <new-node-ip>
```
The join adds the new etcd member (kubeadm adds it as a learner and then promotes it, per the
kubeadm source), writes static pod manifests and registers the node. The uploaded certificate
Secret and its key expire after two hours; re-run `upload-certs` if needed.

## 5. Re-point anything that named the old node
- Load balancer backend pool for :6443 (HAProxy/cloud LB): swap the old IP for the new one.
- Monitoring targets, SSH inventories, backup CronJobs pinned by `nodeName`.
- If the old node had a different IP and you use kube-vip in BGP mode, confirm the peer config.

## Gotchas
- Always remove the dead member before adding a replacement (etcd FAQ): adding first raises the
  quorum requirement and can leave you unable to change membership.
- A node that is merely NotReady (not destroyed) should be fixed, not replaced; if it comes back
  after you removed its member, `kubeadm reset` it before anything else.
- The new node's kube-apiserver cert gets SANs from `kubeadm-config`; if the VIP/DNS isn't in
  `apiServer.certSANs`, clients through the LB get x509 errors - fix the ConfigMap before joining.
- Do this one node at a time; two simultaneous replacements on a 3-node cluster = quorum loss.

## Verify
- [ ] `etcdctl member list` shows 3 started members, `endpoint status --cluster` all healthy with identical RAFT INDEX (±few).
- [ ] `kubectl get nodes` shows 3 Ready control-plane nodes; `kubectl -n kube-system get pods -o wide | grep <new-node>` shows apiserver, controller-manager, scheduler, etcd Running.
- [ ] Kill the apiserver pod on one node (`crictl stop`); `kubectl get --raw /readyz` through the LB keeps answering.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: etcd v3.5 FAQ and runtime-reconfiguration page (remove a failed member before adding its replacement, quorum arithmetic), kubeadm HA page (upload-certs, certificate key expires after two hours, join --control-plane --certificate-key), kubeadm source (token create --print-join-command --certificate-key, join --apiserver-advertise-address, join adds an etcd learner then promotes), the certificates reference (etcd healthcheck-client key pair for etcdctl). Removed the unconfirmed kube-vip lease default and etcd error text.

Method: documentation only; no commands were run.
