---
id: computing-software.cybersecurity-defensive.cosign.key-file-format
name: key-file-format
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, key-format, ecdsa-p256, scrypt, pkcs8, pem]
level: advanced
status: docs-checked
description: "How cosign stores keys and which algorithms it generates: encrypted PEM private keys with scrypt and nacl/secretbox, PKIX public keys, ECDSA P-256 with SHA256."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SIGNATURE_SPEC.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key file format

Private keys: PEM, "encrypted under a password using scrypt as a KDF and nacl/secretbox for encryption", header `ENCRYPTED SIGSTORE PRIVATE KEY`.

```
-----BEGIN ENCRYPTED SIGSTORE PRIVATE KEY-----
...
-----END ENCRYPTED SIGSTORE PRIVATE KEY-----
```

Public keys: PEM, standard PKIX, header `PUBLIC KEY`.

Algorithms (README "Intentionally Missing Features"): "cosign only generates ECDSA-P256 keys and uses SHA256 hashes, for both ephemeral keyless signing and managed key signing. Keys are stored in PEM-encoded PKCS8 format." It can still store and retrieve signatures made with other algorithms.

Spec position (SIGNATURE_SPEC): implementations must support at least ECDSA-P256. No information about the signature scheme is included in the object, so clients determine it out-of-band. Signers and verifiers must know the hash algorithm; the digest is calculated with the same algorithm as the OCI registry, which in practice means sha256. The spec says it only requires ECDSA-P256 with SHA256 but will allow other schemes.

Cosign was inspired by tools like minisign and signify (README).

## Checked

2026-11-04. Confirmed against the cosign README and SIGNATURE_SPEC: PEM header, scrypt and nacl/secretbox, PKIX public key header, ECDSA-P256 and SHA256 statement, PKCS8, spec scheme and hash rules, minisign and signify. Removed: the claim that the key file is useless without its password and loss means re-keying, and the sign-blob --signing-algorithm point with its cross-reference (not on the cited pages).
Method: documentation only; no commands were run.
