---
id: computing-software.cloud-infrastructure-engineering.kubernetes.certificate-rotation-and-expiry-management
name: certificate-rotation-and-expiry-management
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pki, certificates, cert-rotation, kubeadm-certs, kubelet-serving-cert, ca-expiry, tls, kubeconfig, certificate-signing-request, csr, cert-manager, kubeadm-certs-renew, check-expiration]
level: advanced
status: docs-checked
description: "Keep a kubeadm cluster's PKI from expiring unnoticed: checking expiry, kubeadm's manual/upgrade-triggered rotation, kubelet auto-rotation, and the 1-year CA renewal cliff."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/setup/best-practices/certificates/", "https://kubernetes.io/docs/tasks/tls/certificate-rotation/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Certificate rotation and expiry management

**Goal:** no cluster component ever goes down because a certificate silently expired,
the classic failure where an untouched cluster stops working a year after it was built.

## 1. What has what lifetime, by default
- kubeadm-generated **leaf certificates** (API server, kubelet client certs, scheduler and
  controller-manager client certs, etcd certs, front-proxy certs): **1 year** by default
  (`certificateValidityPeriod: 8760h` in `ClusterConfiguration`).
- The **root CAs**: **10 years** by default (`caCertificateValidityPeriod: 87600h`). CA expiry
  catches people off guard: a cluster can run for years of patch upgrades with nobody
  thinking about the CA until the date arrives.
- kubeadm **renews all the certificates it manages during a control plane upgrade**
  (`kubeadm upgrade apply` and `kubeadm upgrade node`; opt out with
  `--certificate-renewal=false`). The documentation describes this as designed for the
  simple case: if you upgrade regularly (less than 1 year between upgrades), kubeadm keeps
  the certificates current. A cluster that stops upgrading also stops renewing.
- **Kubelet client certificates** are not in the `check-expiration` list because kubeadm
  configures the kubelet for automatic renewal with rotatable certificates under
  `/var/lib/kubelet/pki`.
- **Kubelet serving certificates** are different: with `serverTLSBootstrap: true` they are
  requested through the certificates API (signer `kubernetes.io/kubelet-serving`), and the
  default signer in kube-controller-manager does **not** auto-approve them. Someone or a
  third-party approver must run `kubectl certificate approve <csr>`, including at each
  rotation (kubeadm sets `rotateCertificates: true`).

## 2. Checking expiry before it is an emergency
```bash
kubeadm certs check-expiration
```
Shows the expiry of the certificates in `/etc/kubernetes/pki` and of the client certificates
embedded in `admin.conf`, `controller-manager.conf` and `scheduler.conf`; it also tells you
when a certificate is externally managed. Run it on every control-plane node, since each
node holds its own copies.
- Anything kubeadm does not manage (hand-made certificates, cert-manager-issued webhook
  certificates, external CA material) must be checked by its own mechanism.
- Alert well ahead of expiry (weeks, not hours): renewal needs a coordinated restart of
  control-plane static pods on every node.

## 3. Manual rotation (without an upgrade)
```bash
kubeadm certs renew all              # every kubeadm-managed certificate on this node
# or one: kubeadm certs renew apiserver
```
- Run it on **all** control-plane nodes in a replicated control plane.
- Renewal uses the CA key and certificate in `/etc/kubernetes/pki`; attributes such as
  common name, organization and SANs come from the existing certificates, not from the
  `kubeadm-config` ConfigMap (keep the ConfigMap in sync anyway).
- The renew subcommands cover the certificates embedded in `admin.conf`,
  `super-admin.conf`, `controller-manager.conf` and `scheduler.conf` as well as the PKI
  files, so no separate kubeconfig regeneration is needed.
- Restart the control-plane static pods afterwards, because dynamic certificate reload is not
  supported for all components. kubectl cannot restart static pods: temporarily move a
  component's manifest out of `/etc/kubernetes/manifests/`, wait about 20 seconds
  (the kubelet `fileCheckFrequency`), then move it back, one component at a time.
- If you copied `admin.conf` to `$HOME/.kube/config`, copy the renewed file there again.

## 4. The CA-expiry cliff
- `kubeadm certs renew` re-signs leaf certificates with the **existing** CA; it does not
  replace the CA. Replacing a CA is the manual multi-step procedure in
  `computing-software.cloud-infrastructure-engineering.kubernetes.cluster-ca-rotation`
  (distribute a CA bundle, re-issue leaf certificates, remove the old CA).
- Anything that pinned the old CA (`--discovery-token-ca-cert-hash`, the `cluster-info`
  ConfigMap, external systems trusting the cluster CA) needs updating too.
- Track each CA's expiry date as its own calendar item, years ahead.

## Gotchas
- A cluster pinned to one Kubernetes version for over a year skips the upgrade-time
  renewal; `check-expiration` has to run on its own schedule, not only around upgrades.
- Certificates managed externally (external CA mode) are reported by kubeadm but must be
  renewed with your own tooling.
- A renewed certificate on disk is not in use until the static pod has restarted.

## Verify
- [ ] `kubeadm certs check-expiration` runs on a schedule on every control-plane node.
- [ ] An alert fires weeks before any kubeadm-managed certificate expires.
- [ ] Kubelet serving-certificate CSRs (if `serverTLSBootstrap` is on) are approved by a
      known mechanism.
- [ ] Each CA's expiry date is tracked separately from leaf certificates.
- [ ] `kubeadm certs renew all` plus the static-pod restart has been rehearsed on a
      non-production control plane.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm source: kubeadm-certs task page (1-year leaf and 10-year CA defaults, check-expiration scope, automatic renewal during upgrade and --certificate-renewal=false, manual renewal on all control-plane nodes, static-pod restart via manifest move and 20-second fileCheckFrequency, kubelet serving CSRs not auto-approved), kubeadm certs reference (renew subcommands include admin.conf, super-admin.conf, controller-manager.conf, scheduler.conf) and kubeadm constants. Corrected the earlier claim that renew does not touch kubeconfig certificates and the claim that kubelet serving certificates self-approve.

Method: documentation only; no commands were run.
