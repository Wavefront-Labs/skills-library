---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-external-ca-and-generate-csr
name: kubeadm-external-ca-and-generate-csr
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kubeadm, external-ca, generate-csr, pki, certificates]
level: practitioner
status: docs-checked
description: "Run kubeadm with an external CA whose key never touches the nodes, using kubeadm certs generate-csr and pre-created certificates and kubeconfigs."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/implementation-details/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubeadm with an external CA

## How kubeadm detects it
If `/etc/kubernetes/pki/ca.crt` exists and `ca.key` does not, and all other certificates and kubeconfig files are
in place, kubeadm activates external CA mode and proceeds without the CA key. Only the root cluster CA can be
supplied without its key (kubeadm docs: not other cert pairs). The `csrsigner` controller in kube-controller-manager
is not started in this mode.

## Generate CSRs and keys
```bash
kubeadm certs generate-csr --config kubeadm.yaml \
  --cert-dir /tmp/k8s/pki --kubeconfig-dir /tmp/k8s
ls /tmp/k8s/pki/*.csr /tmp/k8s/*.conf.csr
```
Send the CSRs to the CA team; they sign with the right usages
(serverAuth for apiserver and etcd server, clientAuth for kubelet-client, admin, etc).
Place signed certs next to the keys, embed client certs into the `.conf` files, then
copy everything into `/etc/kubernetes` and run `kubeadm init --config kubeadm.yaml`.

## Required SANs
The Kubernetes PKI page lists the SANs each certificate needs, for example the API server certificate needs the
hostname, host IP and advertise IP, plus the `controlPlaneEndpoint` and `certSANs` values from your kubeadm
configuration, which the CSRs generated from `--config` include.

## Day 2
```bash
kubeadm certs check-expiration     # shows EXTERNALLY MANAGED for these certs
```
`kubeadm certs renew` cannot renew externally signed certificates (kubeadm cannot manage certificates signed by an
external CA); generate new CSRs and have them signed before expiry, and monitor expiry yourself.

## Gotchas
- In external CA mode run kube-controller-manager standalone with `--controllers=csrsigner` pointing at the CA
  certificate and key, as the kubeadm docs describe, if you need the in-cluster CSR signer (for example for
  kubelet certificates).

## Checked

Date: 2026-10-26. Documentation release: Kubernetes website docs (kubernetes/website main, 2026-10-26).

Fixed: only the root cluster CA can be supplied without its key (the docs say this is not available for other cert pairs), so the claim that `front-proxy-ca` and `etcd/ca` behave the same way was removed; in external CA mode the `csrsigner` controller in kube-controller-manager is not started, and the docs say to run controller-manager standalone with `--controllers=csrsigner` pointing at the CA, which replaces the vague kubelet signer remark. Confirmed: external CA mode is entered when `ca.crt` exists without `ca.key` and all other certificates and kubeconfig files are in place; `kubeadm certs generate-csr` flags `--config`, `--cert-dir`, `--kubeconfig-dir`, partial kubeconfig files with an accompanying `.csr`, signed certificates saved with a `.crt` extension next to the keys and base64 encoded into `client-certificate-data`; `kubeadm certs check-expiration` shows EXTERNALLY MANAGED; kubeadm cannot manage certificates signed by an external CA, renewal is by new CSRs; PKI table of usages and SANs. Removed as unconfirmed: the intermediate CA claim and the apiserver SAN list.

Method: documentation only; no commands were run.
