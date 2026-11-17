---
id: computing-software.cloud-infrastructure-engineering.knative.internal-tls-and-trust
name: internal-tls-and-trust
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [cluster-local-domain-tls, system-internal-tls, ca-bundle, trust-bundle, kourier]
level: advanced
status: docs-checked
description: "Enable cluster-local-domain-tls and system-internal-tls and handle CA trust."
sources:
  - https://knative.dev/docs/serving/encryption/system-internal-tls/
  - https://knative.dev/docs/serving/encryption/cluster-local-domain-tls/
  - https://knative.dev/docs/serving/encryption/encryption-overview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt in-cluster traffic and traffic between Knative components.

Both features need cert-manager and the Knative cert-manager integration installed and configured first.

Cluster-local domain TLS: add `cluster-local-domain-tls: Enabled` under `data` in the `config-network` ConfigMap in `knative-serving`, then restart the controller to start the integration. The page warns that this feature is currently supported only with Kourier and Istio as the networking layer.

System-internal TLS: add `system-internal-tls: Enabled` in the same ConfigMap, then restart the activator and the controller. The page warns that this feature is currently supported only with Kourier as the networking layer, which is narrower than the cluster-local page (Kourier and Istio).

```yaml
data:
  system-internal-tls: Enabled
```

Trust: Knative automatically trusts the CA that signed the certificates if the cert-manager issuer places the CA directly in the `ca.crt` field of the certificate Secret. Regardless, cluster admins should always provide a trust bundle, as the cert-manager integration page describes under managing trust and rotation without downtime. cert-manager's documentation also strongly recommends this to avoid rotation issues.

Components consume and trust a `CABundle` supplied by the administrator. Each connection is verified using specific SANs, so every component must trust the CA, possibly the full chain.

Callers of cluster-local endpoints must trust the CA too; trust-manager is one way to distribute it.

## Checked

2026-11-04. Confirmed against the system-internal encryption, cluster-local domain encryption and encryption overview pages (knative/docs source): cert-manager and the Knative cert-manager integration as prerequisites, `cluster-local-domain-tls: Enabled` and `system-internal-tls: Enabled` in `config-network` in `knative-serving`, restarting the controller (and the activator for system-internal), the supported networking layers (Kourier and Istio for cluster-local, Kourier only for system-internal), the automatic-trust condition with `ca.crt`, the advice to always provide a trust bundle, the `CABundle` and specific-SAN behaviour, and trust-manager as one option. Replaced the vague warning mention with the actual supported-layer statement. Nothing else removed.

Method: documentation only; no commands were run.
