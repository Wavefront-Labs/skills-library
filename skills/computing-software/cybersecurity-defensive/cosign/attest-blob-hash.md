---
id: computing-software.cybersecurity-defensive.cosign.attest-blob-hash
name: attest-blob-hash
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, attest-blob, blob-hash, statement, predicate]
level: practitioner
status: docs-checked
description: "Attest a file with cosign attest-blob: --predicate or --statement, --hash for artifacts stored elsewhere, bundle output and typed predicates."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest-blob.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# attest-blob

```
cosign attest-blob --predicate <FILE> --type <TYPE> --key cosign.key --bundle <path> <BLOB>
echo <PAYLOAD> | cosign attest-blob --predicate - --yes
```

Flags worth knowing:
- `--hash string`: "hash of blob in hexadecimal (base16). Used if you want to sign an artifact stored elsewhere and have the hash", so you need not have the file locally.
- `--predicate` path to predicate file; `--statement` path to a complete statement file.
- `--type` as for `attest` (default `custom`).
- `--bundle` writes the verification material.
- `--signing-config` path to a signing config file; "Must provide --bundle".
- Key sources: local key, `awskms://`, `azurekms://`, `gcpkms://`, `hashivault://`, or keyless with the OIDC flags.

Verify with `cosign verify-blob-attestation` (see verify-blob-attestation-digest).

On verification, `verify-blob-attestation --check-claims` uses either a provided digest and digest algorithm or the blob's sha256 digest.

## Checked

2026-11-04. Confirmed on the cosign attest-blob and verify-blob-attestation reference pages: usage lines, `--hash` text, `--predicate`, `--statement`, `--type` default custom, `--bundle`, `--signing-config` text, key sources and the `--check-claims` text. Removed: the claim that the statement subject is the blob digest and the guidance about matching algorithms beyond what the check-claims text states.

Method: documentation only; no commands were run.
