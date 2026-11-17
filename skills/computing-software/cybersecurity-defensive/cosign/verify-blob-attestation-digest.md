---
id: computing-software.cybersecurity-defensive.cosign.verify-blob-attestation-digest
name: verify-blob-attestation-digest
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, verify-blob-attestation, digest-alg, in-toto-subject, bundle]
level: advanced
status: docs-checked
description: "Verify a blob attestation bundle and bind it to a file or a given digest with --digest and --digestAlg, including what --check-claims=false skips."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-blob-attestation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# verify-blob-attestation

```
cosign verify-blob-attestation --bundle artifact.sigstore.json \
  --certificate-identity foo@example.com \
  --certificate-oidc-issuer https://accounts.google.com <blob>

cosign verify-blob-attestation --bundle artifact.sigstore.json --key cosign.pub <blob>
```

Signed material comes from `--bundle`. The blob is a file path.

Binding the artifact:
- `--check-claims` (default true) "verifies the digest exists in the in-toto subject (using either the provided digest and digest algorithm or the provided blob's sha256 digest)".
- `--digest` and `--digestAlg` give a digest "instead of providing a blob", so you can verify without the file.
- `--check-claims=false` verifies only the DSSE envelope; the attestation could then be about a different artifact.

Also: `--type` (default `custom`), KMS and Kubernetes Secret key references, `--trusted-root`, `--use-signed-timestamps`, GitHub workflow claim flags, `--insecure-ignore-tlog`.

Note the camel-case flag name `--digestAlg`. Keep `--check-claims` on in gates.

## Checked

2026-11-08. Read in full: the `cosign verify-blob-attestation` reference (raw, sigstore/cosign). Confirmed the examples, `--check-claims` text and default, `--digest`, `--digestAlg`, `--type` default and the other flags listed. Replaced "GitLab" with "Kubernetes Secret" because the `--key` text names only KMS URI and Kubernetes Secret.

Method: documentation only; no commands were run.
