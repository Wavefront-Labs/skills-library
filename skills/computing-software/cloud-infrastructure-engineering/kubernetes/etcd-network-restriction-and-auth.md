---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-network-restriction-and-auth
name: etcd-network-restriction-and-auth
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd, etcd-firewall, etcd-port-restriction, etcd-auth, etcd-role, mtls, cks, client-cert-auth]
level: advanced
status: docs-checked
description: "Lock down etcd access: firewall 2379/2380 to control-plane peers only, require client cert auth, separate CAs, and when etcd's own RBAC users/roles help (non-Kubernetes clients)."
sources: ["https://kubernetes.io/docs/reference/networking/ports-and-protocols/", "https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/", "https://etcd.io/docs/v3.6/op-guide/security/", "https://etcd.io/docs/v3.6/op-guide/authentication/rbac/", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.10/etcd.yaml", "https://kubernetes.io/docs/concepts/services-networking/network-policies/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Restricting etcd access: network and authentication

Read access to etcd = every Secret in the cluster; write access = cluster-admin. kube-apiserver
is the only legitimate client.

## Network
| Port | Who may connect |
|---|---|
| 2379 (client) | kube-apiserver hosts (and backup jobs on those hosts); in stacked kubeadm that's localhost + other CP nodes |
| 2380 (peer) | other etcd members only |
| 2381 (metrics; kubeadm sets `--listen-metrics-urls=http://127.0.0.1:2381`, plain HTTP) | localhost by default; widening it exposes metrics without TLS, so restrict it to Prometheus |

Use the host firewall to allow 2379-2380 only from the control plane nodes (Kubernetes ports table: the etcd
server client API is used by kube-apiserver and etcd), and avoid listening on all interfaces where it is not
needed.
Cloud: security groups / firewall rules so only CP nodes reach 2379-2380; workers never need it.
Check that pods cannot reach it from a worker. NetworkPolicy behaviour for hostNetwork pods is undefined
(Kubernetes docs), so rely on the host firewall rather than NetworkPolicy.

## Transport and client auth (mandatory)
```
--cert-file / --key-file                  # server cert
--client-cert-auth=true --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
--peer-cert-file / --peer-key-file --peer-client-cert-auth=true --peer-trusted-ca-file=...
```
kubeadm uses a **separate etcd CA** (`/etc/kubernetes/pki/etcd/ca.crt`): certs from the
cluster CA (user client certs) can't talk to etcd. Keep it that way; never reuse the main CA.
`--auto-tls`/`--peer-auto-tls` (self-signed, unverified) must be off (CIS 2.3/2.6).

## etcd RBAC (users/roles)
With client-cert auth, the cert CN is the etcd user. etcd's own auth adds roles with key-range
permissions — useful when **other** systems share an etcd (not recommended) or for read-only
backup users:
```bash
etcdctl role add root ; etcdctl user add root --new-user-password=... ; etcdctl user grant-role root root
etcdctl role add backup ; etcdctl role grant-permission backup --prefix=true read /
etcdctl user add backup --no-password ; etcdctl user grant-role backup backup   # cert CN=backup
etcdctl auth enable
```
The Kubernetes etcd page states that etcd authentication (users and roles) is not planned for Kubernetes, so
Kubernetes clusters rely on mutual TLS, a separate etcd CA and network restriction. Do not enable etcd
auth on the cluster's own etcd without testing it on a copy.

## Verify
- [ ] From a worker node and a pod: connection to 2379 is refused or times out.
- [ ] `etcdctl --endpoints=https://<cp>:2379 endpoint health` without client certs fails (`bad certificate`).
- [ ] kube-bench etcd checks 2.1-2.7 pass.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master); etcd mixin (etcd-io/etcd main); kube-prometheus-stack chart values (prometheus-community/helm-charts main).

Fixed: the role `root` must exist before `user grant-role root root` (`etcdctl role add root` first, as in the etcd RBAC guide); the Kubernetes etcd page states that etcd authentication is not planned for Kubernetes, so the claim that enabling etcd auth needs the API server certificate mapped to a root user was replaced; hostNetwork pods: NetworkPolicy behaviour is undefined (Kubernetes docs), not simply bypassed. Confirmed: etcd server client API ports 2379-2380 for kube-apiserver and etcd; kubeadm's default etcd arguments (`--cert-file`, `--key-file`, `--client-cert-auth`, `--trusted-ca-file`, `--peer-*`, metrics on 127.0.0.1:2381) and its separate etcd CA; CIS items 2.1 to 2.7 in kube-bench (2.3 `--auto-tls`, 2.5 `--peer-client-cert-auth`, 2.6 `--peer-auto-tls`, 2.7 unique CA); etcd Common Name based user mapping with `--client-cert-auth=true`; `etcdctl user add --no-password`, `role grant-permission --prefix=true`, `auth enable`. Removed as unconfirmed: the nftables rules, the `ss` and `nc` commands and the remark about a metrics proxy.

Method: documentation only; no commands were run.
