---
id: computing-software.cloud-infrastructure-engineering.external-secrets-operator.external-secrets-operator-template-rsadecrypt-pushsecret
name: external-secrets-operator-template-rsadecrypt-pushsecret
category: computing-software
field: cloud-infrastructure-engineering
product: external-secrets-operator
tags: [templating, rsadecrypt, pushsecret, engineversion]
level: sme
status: docs-checked
description: "Decrypt RSA-encrypted provider values in a template with rsaDecrypt, template PushSecret output, and know which sprig functions are removed."
sources:
  - https://raw.githubusercontent.com/external-secrets/external-secrets/main/docs/guides/templating.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rsaDecrypt` is used as `<privateKeyPEM | rsaDecrypt "<SCHEME>" "<HASH>" <ciphertext>>` with strings such as `"RSA-OAEP"` and `"SHA1"`. Requirements: `spec.target.template.engineVersion: v2`, an RSA private key in PEM without passphrase (from another reference in the same ExternalSecret), and binary ciphertext matching the key pair and algorithm. Providers often return base64, so either decode in the template with `b64dec` or set `decodingStrategy: Base64` on the `spec.data` remoteRef. A mismatch makes decryption fail and reconciliation retries.

PushSecret uses the same template structure, so the features above also apply to the value written to the provider.

For security, `env`, `expandenv`, `getHostByName` and `fail` were removed from the sprig function set; report failures through reconciliation diagnostics instead.

## Checked

2026-11-03. Claims were read against guides/templating.md in the external-secrets docs source. Removed: nothing.

Method: documentation only; no commands were run.
