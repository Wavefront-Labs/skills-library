---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-pkcs12-functions
name: external-secrets-operator-template-pkcs12-functions
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, pkcs12, pem, certificates]
level: advanced
status: docs-checked
description: "Convert between PKCS#12 archives and PEM with the pkcs12key, pkcs12cert and pemToPkcs12 template functions."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Template helper functions handle certificate formats:
- `pkcs12key` / `pkcs12keyPass`: extract all private keys from a PKCS#12 archive as PKCS#8 PEM (the Pass variant takes the archive password).
- `pkcs12cert` / `pkcs12certPass`: extract and, where possible, order the certificates as leaf, intermediate(s), root. Disjunct or multiple leaf certificates are returned as-is.
- `pemToPkcs12` / `pemToPkcs12Pass`: build a base64 PKCS#12 archive from a PEM certificate and key.
- `fullPemToPkcs12` / `...Pass`: the same from a PEM certificate chain and key.
- `pemTruststoreToPKCS12` / `...Pass`: build a PKCS#12 truststore from PEM certificates.

The documented use is extracting keys and certificates from a PKCS#12 archive and storing them as PEM. In the same engine you also get 200+ sprig functions.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: an unsupported Java keystore use case.

Method: documentation only; no commands were run.
