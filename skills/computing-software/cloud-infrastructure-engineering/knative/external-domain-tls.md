---
id: computing-software.cloud-infrastructure-engineering.knative.external-domain-tls
name: external-domain-tls
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [external-domain-tls, wildcard-certificate, namespace-wildcard-cert-selector, dns-01, certificate-provisioning]
level: advanced
status: docs-checked
description: "Enable automatic per-Service or per-namespace wildcard certificates for the external domain."
sources:
  - https://knative.dev/docs/serving/encryption/external-domain-tls/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Knative Services over HTTPS on a custom external domain.

Requirements: Knative Serving installed, a custom external domain configured, DNS set up for that domain, and a networking layer such as Kourier, Istio with SDS v1.3 or higher, or Contour v1.1 or higher. Knative can use custom certificates or automatically generated ones.

Automatic provisioning first needs cert-manager and the Knative cert-manager integration installed. It can request either one certificate per Service or one wildcard certificate per namespace; only one mode can be active at a time.

Per Service: set `external-domain-tls: Enabled` under `data` in the `config-network` ConfigMap (namespace `knative-serving`), then restart the controller:

```bash
kubectl rollout restart deploy/controller -n knative-serving
```

Per-namespace wildcard: this works only with the DNS-01 challenge, not HTTP-01. Namespaces are chosen by label through `namespace-wildcard-cert-selector` in `config-network`:
- `""` disables the feature (default).
- `{}` enables it for all namespaces.

Opt-out example:

```yaml
namespace-wildcard-cert-selector: |-
  matchExpressions:
  - key: "networking.knative.dev/disableWildcardCert"
    operator: "NotIn"
    values: ["true"]
```

This selects every namespace whose label value is not `"true"`. You can instead match names with `kubernetes.io/metadata.name` and operator `In`. Restart the controller after changing the selector, as for the per-Service mode.

To opt a single Service or Route out while automatic provisioning is on, add the annotation `networking.knative.dev/disable-external-domain-tls: "true"`; its URL then becomes `http`.

## Checked

2026-11-04. Confirmed against the Configure external domain encryption page (knative/docs source): requirements (including Istio SDS v1.3 or higher and Contour v1.1 or higher), custom or automatic certificates, cert-manager and integration prerequisite, per-Service versus per-namespace wildcard with only one active, `external-domain-tls: Enabled` in `config-network`, the controller restart, DNS-01 only for wildcard certificates, `namespace-wildcard-cert-selector` values `""` and `{}`, and the opt-out and name-based examples. Added the controller restart for the wildcard mode and the per-Service disable annotation, both on the same page. Nothing removed.

Method: documentation only; no commands were run.
