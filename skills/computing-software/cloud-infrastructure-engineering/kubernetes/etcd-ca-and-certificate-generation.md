---
id: computing-software.cloud-infrastructure-engineering.kubernetes.etcd-ca-and-certificate-generation
name: etcd-ca-and-certificate-generation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, etcd-security, etcd-ca, pki, kubeadm, etcd-certificates]
level: practitioner
status: docs-checked
description: "Create and maintain a dedicated etcd CA and its server, peer and client certificates with kubeadm phases or openssl, with the SANs and usages etcd needs."
sources: ["https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/", "https://etcd.io/docs/v3.6/op-guide/security/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# etcd CA and certificates

Use a CA that only etcd trusts. If etcd trusted the cluster CA, any certificate the cluster
signs (including CSR-approved user certs) could talk to etcd.

## kubeadm layout
| File | Purpose | Usage |
|---|---|---|
| `pki/etcd/ca.crt/.key` | etcd CA | |
| `pki/etcd/server.crt` | etcd client-facing server | server + client auth, SANs: hostname, node IP, `localhost`, `127.0.0.1`, `::1` |
| `pki/etcd/peer.crt` | member-to-member | server + client auth, SANs: hostname, node IP |
| `pki/etcd/healthcheck-client.crt` | liveness probes | client auth |
| `pki/apiserver-etcd-client.crt` | apiserver to etcd | client auth |

```bash
kubeadm init phase certs etcd-ca
kubeadm init phase certs etcd-server --config kubeadm.yaml
kubeadm init phase certs etcd-peer --config kubeadm.yaml
kubeadm init phase certs etcd-healthcheck-client
kubeadm init phase certs apiserver-etcd-client
```
Extra SANs: `etcd.local.serverCertSANs` and `peerCertSANs` in ClusterConfiguration.

## External etcd
For an external etcd cluster, the kubeadm external etcd guide generates the same certificates on each
host with `kubeadm init phase certs etcd-server`, `etcd-peer` and `etcd-healthcheck-client` using a
per-host kubeadm configuration (its `serverCertSANs` and `peerCertSANs` list the host IP), and
`apiserver-etcd-client` for the control plane. Copy the etcd CA to the control plane nodes only as
`ca.crt`; the key stays with whoever issues etcd certificates.

## Day 2
Renew each certificate with its own command (`kubeadm certs renew` has one sub-command per
certificate, plus `all`):
```bash
kubeadm certs renew etcd-server
kubeadm certs renew etcd-peer
kubeadm certs renew etcd-healthcheck-client
kubeadm certs renew apiserver-etcd-client
```
Then restart the control plane static pods (kubeadm docs: move the manifests out of
`/etc/kubernetes/manifests` and back). Leaf certificates default to one year and the etcd CA to ten
years; check both with `kubeadm certs check-expiration`.

## Verify
```bash
openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -noout -issuer -text
```
The issuer is the etcd CA, not the cluster CA; check the SAN list and the server and client usages in the text output.

## Checked

Date: 2026-10-26. Documentation release: etcd v3.6 docs (etcd-io/website, repository head 2026-10-23); Kubernetes website docs (kubernetes/website main, 2026-10-26); kubeadm and kube-apiserver source (kubernetes/kubernetes master).

Confirmed: the file layout, usages and SANs table (Kubernetes PKI certificates page: etcd server and peer certificates are server+client with the hostname, host IP, localhost and 127.0.0.1; healthcheck-client and apiserver-etcd-client are client only); the five `kubeadm init phase certs` sub-commands exist; `etcd.local.serverCertSANs` and `peerCertSANs` appear in the kubeadm external etcd guide; CA validity default 87600h (10 years) and leaf default 8760h (1 year); `kubeadm certs renew` has one sub-command per certificate; kubeadm docs say to restart the control plane pods after renewal. Fixed: `kubeadm certs renew` takes one certificate name per invocation, not a list. Removed as unconfirmed: the openssl signing example and the `-ext` verification flag.

Method: documentation only; no commands were run.
