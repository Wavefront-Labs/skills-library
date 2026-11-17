---
id: computing-software.systems-network-administration.pki-tls-administration.k8s-cluster-pki-rotation
name: k8s-cluster-pki-rotation
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [k8s-cluster-pki-rotation, pki-kubernetes, kubernetes, kubeadm, certificates, rotation, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Check and renew Kubernetes control plane certificates with kubeadm, restart static pods, and approve kubelet serving CSRs."
sources:
  - https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes control plane PKI
Goal: no cluster outage from expired internal certificates.
```
kubeadm certs check-expiration
kubeadm certs renew all        # on every control-plane node
```
- kubeadm client certificates expire after 1 year by default (`certificateValidityPeriod: 8760h`); CA certificates default to 10 years (`caCertificateValidityPeriod: 87600h`).
- `check-expiration` covers the certificates under `/etc/kubernetes/pki` and those embedded in `admin.conf`, `controller-manager.conf` and `scheduler.conf`, and marks any that are externally managed (kubeadm cannot manage certificates signed by an external CA). `kubelet.conf` is not listed because the kubelet rotates its client certificate under `/var/lib/kubelet/pki`.
- kubeadm renews all certificates during a control plane upgrade; regular upgrades (less than a year apart) therefore keep them current. Opt out with `--certificate-renewal=false` on `kubeadm upgrade apply` or `kubeadm upgrade node`.
- `kubeadm certs renew` signs with the CA files in `/etc/kubernetes/pki`, takes names and SANs from the existing certificates, and must be run on every control-plane node of a replicated control plane.
- After renewing, restart the control plane pods, since dynamic reload is not supported for all components. Static pods cannot be deleted with kubectl: move the manifest out of `/etc/kubernetes/manifests/`, wait about 20 seconds (`fileCheckFrequency`), then move it back and wait again.
- Kubelet serving certificates: set `serverTLSBootstrap: true` in the KubeletConfiguration (the `kubelet-config` ConfigMap and `/var/lib/kubelet/config.yaml` on each node, then restart the kubelet). The default kube-controller-manager signer for `kubernetes.io/kubelet-serving` does not auto-approve these CSRs, so list them with `kubectl get csr` and approve with `kubectl certificate approve <CSR-name>` or use a third-party approver. kubeadm sets `rotateCertificates: true`, so new CSRs appear near expiry and must be approved.
Gotcha: after renewing `admin.conf`, any copy such as `$HOME/.kube/config` still holds the old certificate; copy the new file over it (and fix its ownership).
Verify:
- [ ] `kubeadm certs check-expiration` shows new expiry dates for every certificate.
- [ ] kubectl works with the refreshed kubeconfig after the control plane pods restart.

## Checked
Confirmed 2026-11-08 against the kubeadm "Certificate Management" page: validity defaults, check-expiration scope, automatic renewal on upgrade, manual renewal and static-pod restart, serverTLSBootstrap and CSR approval, admin.conf copy. Removed (not on the page): the `kubernetes.io/kube-apiserver-client` signer name, the 300-day verify threshold, the backup advice and the `/readyz` check.
Method: docs-only read of cited pages, 2026-11-08
