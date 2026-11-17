---
id: computing-software.cloud-infrastructure-engineering.zot.signature-verification-trust
name: signature-verification-trust
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, trust-extension, cosign-keys, notation-certificates, signature-verification, image-trust]
level: practitioner
status: docs-checked
description: "Enable Zot's trust extension and upload cosign public keys or notation certificates so signed images show as trusted in GraphQL and the UI."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/verifying-signatures.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/mirroring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable under `extensions`:

```json
"trust": { "enable": true, "cosign": true, "notation": true }
```

`cosign` verifies with uploaded public keys; `notation` verifies with uploaded certificates.

Upload material:

```
curl --data-binary @file.pub "http://localhost:8080/v2/_zot/ext/cosign"
curl --data-binary @certificate.crt "http://localhost:8080/v2/_zot/ext/notation?truststoreType=ca"
```

- Uploaded cosign keys are stored in `_cosign` and notation certificates under `_notation/truststore/x509/{truststoreType}/default`, below `rootDir` (or in the Secrets Manager). `truststoreType` is `ca` when omitted.
- Notation uses a `trustpolicy.json` that zot maintains automatically, with `signatureVerification.level` set to `strict`.
- Cosign v3 Sigstore bundles are verified against uploaded cosign public keys like other key-based signatures.

Check results with GraphQL:

```graphql
{ Image(image: "busybox:latest") { Digest IsSigned Tag SignatureInfo { Tool IsTrusted Author } } }
```

Related: sync `onlySigned: true` copies only notation- or cosign-signed images.

## Checked

2026-11-04. Confirmed against the verifying-signatures page (trust extension, upload endpoints, storage paths, trustpolicy.json strict level, Sigstore bundles, GraphQL query) and the mirroring page for onlySigned. Removed claims the pages do not state.

Method: documentation only; no commands were run.
