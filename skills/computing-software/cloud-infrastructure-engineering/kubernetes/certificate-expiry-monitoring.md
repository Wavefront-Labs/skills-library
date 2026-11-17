---
id: computing-software.cloud-infrastructure-engineering.kubernetes.certificate-expiry-monitoring
name: certificate-expiry-monitoring
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, certificates, x509-certificate-exporter, cert-expiry-monitoring, prometheus]
level: practitioner
status: docs-checked
description: "Alert before Kubernetes certificates expire: apiserver client-cert metrics, x509-certificate-exporter for node files and Secrets, and cert-manager metrics."
sources: ["https://github.com/enix/x509-certificate-exporter", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://cert-manager.io/docs/devops-tips/prometheus-metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate expiry monitoring

Kubeadm leaf certs last a year and only renew during upgrades or `kubeadm certs renew`.
Clusters not upgraded for a year go down on a predictable date. Monitor it.

## x509-certificate-exporter (files and Secrets)
The chart is published as an OCI artifact; the project's quick install is:
```bash
helm -n monitoring install x509-certificate-exporter \
  oci://quay.io/enix/charts/x509-certificate-exporter
```
The Secrets exporter is enabled by default and watches `kubernetes.io/tls` Secrets. For control-plane
files, the project ships example values at `docs/examples/distros/kubeadm.values.yaml`: a
`hostPathsExporter.daemonSets.controlplane` entry with a control-plane `nodeSelector` and
toleration, `watchFiles` for the `/etc/kubernetes/pki/*.crt` files and the kubelet client
certificate, and `watchKubeconfFiles` for the admin, controller-manager and scheduler kubeconfigs;
pass it with `-f`. The metric `x509_cert_not_after` is a Unix timestamp. Version 4 of the chart changed
some values shapes and retired the Alpine image variant, so read the project's v3 to v4 migration guide
when upgrading.
```yaml
- alert: CertificateExpiringSoon
  expr: (x509_cert_not_after - time()) / 86400 < 28
  labels: {severity: warning}
- alert: CertificateExpiryCritical
  expr: (x509_cert_not_after - time()) / 86400 < 7
  labels: {severity: critical}
```

## Built-in signals
- `apiserver_client_certificate_expiration_seconds` (alpha histogram): remaining lifetime of the
  certificates used to authenticate requests; counts in buckets near zero mean a client
  certificate is close to expiry.
- Kubelet: `kubelet_certificate_manager_client_ttl_seconds` and
  `kubelet_certificate_manager_server_ttl_seconds`.
- cert-manager: `certmanager_certificate_expiration_timestamp_seconds` and
  `certmanager_certificate_ready_status`.

## Process
- Alert at 28 days so there is a full sprint to act; page at 7 days.
- Put `kubeadm certs check-expiration` in a weekly report as a cross-check.
- CA expiry (10 years) is not covered by renewals; track it as a separate long-dated reminder.

## Checked

2026-10-27. Release: Kubernetes v1.37 docs, x509-certificate-exporter v4 chart (main), cert-manager source (main), October 2026
- Confirmed in the Kubernetes kubeadm certificate page that kubeadm leaf certificates expire after 1 year, that kubeadm renews them during control-plane upgrades, that `kubeadm certs renew` and `kubeadm certs check-expiration` exist, and the 10-year default for CA certificates (`caCertificateValidityPeriod: 87600h`).
- Confirmed the metrics `apiserver_client_certificate_expiration_seconds`, `kubelet_certificate_manager_client_ttl_seconds` and `kubelet_certificate_manager_server_ttl_seconds` (Kubernetes metrics reference, alpha), and `certmanager_certificate_expiration_timestamp_seconds` and `certmanager_certificate_ready_status` (cert-manager collector source).
- Corrected the exporter install: the current chart is installed from `oci://quay.io/enix/charts/x509-certificate-exporter` and the old `--set` keys were replaced with the project's kubeadm example values; confirmed `x509_cert_not_after` in the project's metrics reference.

Method: documentation only; no commands were run.
