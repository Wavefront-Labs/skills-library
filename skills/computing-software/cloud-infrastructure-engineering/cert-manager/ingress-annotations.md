---
id: computing-software.cloud-infrastructure-engineering.cert-manager.ingress-annotations
name: ingress-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [ingress-shim, tls-acme, issuer-annotation, cluster-issuer, defaultissuername, annotations]
level: practitioner
status: docs-checked
description: "Get cert-manager Certificates from Ingress resources: issuer annotations, tls.secretName mapping, private-key annotations, tls-acme defaults and no-Certificate debugging."
sources:
  - https://cert-manager.io/docs/usage/ingress/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ingress-shim creates a Certificate in the Ingress namespace named from `tls.secretName`, with SANs from `tls.hosts`. Each Ingress needs a unique `tls.secretName`.

Trigger with one of:
- `cert-manager.io/issuer` (Issuer must be in the Ingress namespace) or `cert-manager.io/cluster-issuer` (cert-manager ClusterIssuers only).
- `cert-manager.io/issuer-kind` and `issuer-group` for out-of-tree issuers.
- `kubernetes.io/tls-acme: "true"`, which only works if a default issuer is set via `ingressShim.defaultIssuerName`, `defaultIssuerKind`, `defaultIssuerGroup` (or container args). Issuer annotations override that default.

Other annotations: `cert-manager.io/common-name`, `duration`, `renew-before`, `usages` (comma-separated), `private-key-algorithm` (`RSA` default, `ECDSA`, `Ed25519`), `private-key-encoding` (`PKCS1` default, `PKCS8`), `private-key-size` (RSA 2048/4096/8192 default 2048; ECDSA 256/384/521 default 256), `private-key-rotation-policy` (`Always` default, `Never`), subject fields, `email-sans`, `revision-history-limit` (minimum 1).

ACME: `acme.cert-manager.io/http01-ingress-class`, `http01-ingress-ingressclassname`, `http01-edit-in-place` (adds the temporary-certificate annotation).

Copying custom annotations onto Certificates needs v1.18.0+ and `--extra-certificate-annotations` (Helm `config.ingressShimConfig.extraCertificateAnnotations`).

No Certificate appearing: confirm an issuer annotation exists (`tls-acme` additionally needs the default issuer above), then read the cert-manager pod logs. Without annotations, create Certificates yourself and reference the Secret.

## Checked

2026-11-03. Confirmed on the cert-manager Ingress page (usage/ingress): ingress-shim behaviour, issuer and cluster-issuer annotations and namespace rules, issuer-kind and group, tls-acme default issuer settings, all listed annotations with their defaults and valid values, v1.18.0 extra annotations flag and Helm key, unique secretName rule. Reworded one troubleshooting clause.
Method: documentation only; no commands were run.
