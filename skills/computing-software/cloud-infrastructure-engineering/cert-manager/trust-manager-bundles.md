---
id: computing-software.cloud-infrastructure-engineering.cert-manager.trust-manager-bundles
name: trust-manager-bundles
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [trust-manager, bundle, usedefaultcas, namespaceselector, jks, pkcs12, ca-bundle]
level: advanced
status: docs-checked
description: "Distribute CA bundles with trust-manager Bundle resources: sources, targets, namespaceSelector, JKS and PKCS12, default CA package upgrades and rotation pitfalls."
sources:
  - https://cert-manager.io/docs/trust/trust-manager/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`Bundle` is `trust.cert-manager.io/v1alpha1`, cluster-scoped.

`sources` (list): `configMap` or `secret` (by name or label `selector`, and `key` or `includeAllKeys`; read from the trust-manager namespace), `inLine` (PEM with at least one certificate), `useDefaultCAs: true`.

`target`: `configMap` (default) or `secret` (needs explicit controller enablement; v0.7.0+), written to an object named after the Bundle under the given `key`; supports `metadata.labels/annotations`. `additionalFormats.jks` (v0.5.0+) and `pkcs12` (v0.7.0+) take `key` and optional `password`; defaults are `changeit` (JKS) and empty (PKCS#12), not security controls. `target.namespaceSelector` supports only `matchLabels`; empty means all namespaces.

Install: `oci://quay.io/jetstack/charts/trust-manager` (for example into `cert-manager`). Default package image values: `defaultPackageImage.repository` and `.tag`. Debian Trixie for chart >= v0.23, Bookworm for >= v0.16 and < v0.23; Bullseye is deprecated. Charts v0.25.0 and earlier install an affected package. To update: `helm get values`, set the tag, and pin `--version` to the installed trust-manager so the controller does not upgrade; recover from a bad tag with `helm rollback`.

Pitfalls:
- Sourcing a cert-manager Secret root directly distrusts a rotated root instantly. Copy roots into a dedicated source and stage old plus new roots.
- `tls.crt` may hold intermediates; `ca.crt` is best-effort. Keep intermediates out of trust stores.

## Checked

2026-11-03: Confirmed against the trust-manager page: `Bundle` `trust.cert-manager.io/v1alpha1`, cluster scoped, source types and the name/selector and key/includeAllKeys rules, target ConfigMap default and Secret targets from v0.7.0, JKS from v0.5.0 and PKCS#12 from v0.7.0 with default passwords `changeit` and empty, `namespaceSelector` `matchLabels` only and empty meaning all namespaces, the OCI chart, `defaultPackageImage` values, Trixie and Bookworm defaults by chart version, Bullseye deprecation, v0.25.0-and-earlier affected package, the Helm values upgrade procedure and `helm rollback`, and the rotation and `tls.crt`/`ca.crt` guidance. Nothing removed.

Method: documentation only; no commands were run.
