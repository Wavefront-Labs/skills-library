---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubernetes-pki-layout
name: kubernetes-pki-layout
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, certificates, pki-layout, kubernetes-pki-files, kubeadm-certs]
level: practitioner
status: docs-checked
description: "Map every certificate in a kubeadm cluster's /etc/kubernetes/pki to the component that uses it, its signer and what breaks when it expires."
sources: ["https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes PKI layout (kubeadm)

## CAs
| File | Signs |
|---|---|
| `pki/ca.crt/key` | apiserver serving, apiserver-kubelet-client, all component kubeconfig client certs, kubelet client certs |
| `pki/etcd/ca.crt/key` | etcd server, peer, healthcheck-client, apiserver-etcd-client |
| `pki/front-proxy-ca.crt/key` | front-proxy-client (aggregation layer) |
| `pki/sa.key/sa.pub` | not a CA: key pair signing ServiceAccount tokens |

CAs are valid 10 years and leaf certificates 1 year by default (`caCertificateValidityPeriod` and `certificateValidityPeriod` in `ClusterConfiguration`).

## Leaf certificates
| File | Used by | Purpose |
|---|---|---|
| `apiserver.crt` | kube-apiserver | serving cert, SANs incl. service IP, `kubernetes.default...`, node IP, endpoint |
| `apiserver-kubelet-client.crt` | kube-apiserver | client to kubelets (logs, exec) |
| `apiserver-etcd-client.crt` | kube-apiserver | client to etcd |
| `front-proxy-client.crt` | kube-apiserver | client to aggregated API servers |
| `etcd/server.crt`, `etcd/peer.crt` | etcd | client-facing and member-to-member TLS |
| `etcd/healthcheck-client.crt` | etcd liveness probe | client |

## Kubeconfigs with embedded client certs
`admin.conf` (group kubeadm:cluster-admins), `super-admin.conf` (system:masters),
`controller-manager.conf`, `scheduler.conf`, and `kubelet.conf` (points to
`/var/lib/kubelet/pki/kubelet-client-current.pem`, auto-rotated).

## What breaks on expiry
- apiserver.crt: every client gets x509 errors.
- apiserver-etcd-client.crt: the API server cannot talk to etcd and fails.
- controller-manager/scheduler kubeconfigs: those components can no longer authenticate to the
  API server, so controllers and scheduling stop working.
- apiserver-kubelet-client: calls from the API server to kubelets (such as `kubectl logs` and
  `exec`) fail.

## Inspect
```bash
sudo kubeadm certs check-expiration
sudo ls -l /etc/kubernetes/pki /etc/kubernetes/pki/etcd
```
Restrict private keys to root; the CIS benchmark has file-permission checks (confirm the exact modes in the benchmark version you use).

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: best-practices certificates page (CA and leaf certificate paths and parent CAs, sa.key and sa.pub, kubeconfig files and their subjects), kubeadm-certs page (admin.conf group kubeadm:cluster-admins, super-admin.conf system:masters, kubelet.conf auto-rotated) and kubeadm source constants (1-year and 10-year validity). Replaced unconfirmed failure-symptom details and the file-mode figure.

Method: documentation only; no commands were run.
