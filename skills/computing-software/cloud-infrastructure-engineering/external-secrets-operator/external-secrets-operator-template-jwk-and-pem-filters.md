---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-jwk-and-pem-filters
name: external-secrets-operator-template-jwk-and-pem-filters
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, jwk, filterpem, certsans]
level: advanced
status: docs-checked
description: "Extract JWK key parts, filter PEM blocks and certificate chains, and read SANs from certificates in ESO templates."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- JWK: extract the public or private part of a JWK and render it as a PKCS#8 private key or a PEM PKIX public key.
- `filterPEM`: keep only PEM blocks of a given type, for example `CERTIFICATE` from a secret holding both a private key and a certificate. If several blocks of that type exist all are returned in order.
- `filterCertChain`: from a chain of `CERTIFICATE` PEM blocks, pick the `leaf`, `intermediate` or `root` certificate(s); it combines with `filterPEM`.
- `certSANs`: list the Subject Alternative Names (DNS names, IP addresses, emails, URIs) of a PEM certificate, combinable with the two filters to inspect only the leaf.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: a closing generalisation about bundles.

Method: documentation only; no commands were run.
