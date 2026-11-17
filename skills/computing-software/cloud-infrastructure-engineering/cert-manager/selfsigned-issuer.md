---
id: computing-software.cloud-infrastructure-engineering.cert-manager.selfsigned-issuer
name: selfsigned-issuer
category: computing-software
field: cloud-infrastructure-engineering
product: cert-manager
tags: [selfsigned, issuer, bootstrap-ca, crldistributionpoints, empty-issuer-dn]
level: intro
status: docs-checked
description: "Use the SelfSigned issuer to bootstrap a root CA for cert-manager, and avoid the empty Issuer DN and trust pitfalls."
sources:
  - https://cert-manager.io/docs/configuration/selfsigned/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Minimal spec: `selfSigned: {}`, valid for an `Issuer` or `ClusterIssuer`, no dependencies. `kubectl get issuers` should show `READY True`.

Certificates are signed with their own private key. A CertificateRequest for a self-signed cert must carry the annotation `cert-manager.io/private-key-secret-name`; the Certificate controller adds it automatically. Optional `spec.selfSigned.crlDistributionPoints` is an array of URL strings.

Bootstrapping a CA: create a `Certificate` with `isCA: true`, `commonName`, `secretName`, `privateKey` (`algorithm: ECDSA`, `size: 256`) and an `issuerRef` to the SelfSigned issuer. Then a CA issuer references it with `ca.secretName`. For a ClusterIssuer the root Secret must be in the `cert-manager` namespace.

Pitfalls:
- Empty Issuer DN: self-signed certs have identical Subject and Issuer, and Subject is unset by default. RFC 5280 requires a non-empty issuer DN, so set `spec.subject` on the Certificate. Since 1.3 cert-manager emits a `BadConfig` warning event when it detects this.
- Clients cannot trust these certs without already holding them; distribute `ca.crt` with trust-manager. Trust-on-first-use is open to man-in-the-middle.
- Production use needs plans for rotation, trust distribution and disaster recovery; a CA issuer is generally preferred.

## Checked

2026-11-03. Confirmed on the cert-manager SelfSigned page (configuration/selfsigned): selfSigned stanza, private-key-secret-name annotation, bootstrap Certificate fields, cert-manager namespace for ClusterIssuer roots, crlDistributionPoints, empty Issuer DN caveat with RFC 5280 and the 1.3 BadConfig event, trust-manager and TOFU remarks. Nothing removed.
Method: documentation only; no commands were run.
