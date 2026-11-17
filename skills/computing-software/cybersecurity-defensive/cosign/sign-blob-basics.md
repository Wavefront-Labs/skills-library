---
id: computing-software.cybersecurity-defensive.cosign.sign-blob-basics
name: sign-blob-basics
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, sign-blob, signing-algorithm, blob, base64-signature]
level: intro
status: docs-checked
description: "Sign arbitrary files with cosign sign-blob using keyless, local key, KMS or hardware key, choose --signing-algorithm and save the bundle."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign-blob.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing blobs

`cosign sign-blob` signs a file and "outputs the base64-encoded signature to stdout".

```
cosign sign-blob --key cosign.key <FILE>
cosign sign-blob --key awskms://[ENDPOINT]/[ID/ALIAS/ARN] <FILE>
cosign sign-blob <FILE> --bundle artifact.sigstore.json --yes     # keyless
```

Prefer `--bundle`: the verify-blob page calls a Sigstore bundle the preferred way to provide verification material, containing the signature, certificate and transparency log proof (see verify-blob-bundle).

`--signing-algorithm` (default `ecdsa-sha2-256-nistp256`), allowed:
- ecdsa-sha2-256-nistp256, ecdsa-sha2-384-nistp384, ecdsa-sha2-512-nistp521
- rsa-sign-pkcs1-2048-sha256, rsa-sign-pkcs1-3072-sha256, rsa-sign-pkcs1-4096-sha256

Other flags: `--sk` and `--slot` for hardware keys, `--identity-token`, the OIDC flags from keyless-signing-flow, `-y` to skip prompts.

Gotchas:
- The verifier must support the signing algorithm you pick.
- To sign an artifact held elsewhere, see attest-blob-hash (`--hash` exists on attest-blob).

## Checked

2026-11-04. Confirmed on the cosign sign-blob reference page (base64 signature to stdout, `--bundle`, `--signing-algorithm` default and the six allowed values, `--sk`, `--slot`, `--identity-token`, `-y`) and in the README keyless blob example. Removed: the claim about the default key pair format.

Method: documentation only; no commands were run.
