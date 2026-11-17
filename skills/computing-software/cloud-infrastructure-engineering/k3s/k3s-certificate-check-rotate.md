---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-certificate-check-rotate
name: k3s-certificate-check-rotate
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, certificate-check, certificate-rotate, cert-expiry]
level: practitioner
status: docs-checked
description: "Check K3s client and server certificate expiry and rotate leaf certificates manually."
sources:
  - https://docs.k3s.io/cli/certificate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lifetimes: client and server certificates last 365 days. Any certificate expired or within 120 days of expiry is renewed automatically each time K3s starts, reusing the existing keys and extending the lifetime. Within 120 days a Kubernetes Warning Event with reason CertificateExpirationWarning is created against the Node. Before the May 2025 releases (v1.33.1+k3s1, v1.32.5+k3s1, v1.31.9+k3s1, v1.30.13+k3s1) the threshold was 90 days.

Check expiry:

```
k3s certificate check --output table
```

Output formatting needs the January 2025 releases (v1.32.0+k3s1, v1.31.5+k3s1, v1.30.9+k3s1, v1.30.13+k3s1); the richer table needs the May 2025 releases. Columns: FILENAME, SUBJECT, USAGES, EXPIRES, RESIDUAL TIME, STATUS. Each file lists the leaf and its CA, so a file appears twice. For odd output use --data-dir for a custom data directory or --debug.

Rotate to new keys and certificates (rather than extending):

```
systemctl stop k3s
k3s certificate rotate
systemctl start k3s
```

Rotate only some: `k3s certificate rotate --service <SERVICE>,<SERVICE>` from admin, api-server, controller-manager, scheduler, k3s-controller, k3s-server, cloud-controller, etcd, auth-proxy, kubelet, kube-proxy.

Metric: k3s_certificate_expiration_seconds exposes remaining lifetime when supervisor metrics are on.

## Checked

2026-11-03: read docs.k3s.io cli/certificate. Confirmed: 365-day lifetime, 120-day renewal window and CertificateExpirationWarning event, the 90-day threshold before the May 2025 releases, and the January 2025 release gate for output formatting.

Method: documentation only; no commands were run.
