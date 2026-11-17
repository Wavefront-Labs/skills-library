---
id: computing-software.cybersecurity-defensive.cosign.download-signature-attestation
name: download-signature-attestation
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, download-signature, download-attestation, predicate-type, platform]
level: practitioner
status: docs-checked
description: "Fetch raw signatures and in-toto attestations from a registry with cosign download signature and download attestation, filtering by predicate type or platform."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_download_signature.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_download_attestation.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_download.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# download signature and attestation

```
cosign download signature <image uri>
cosign download attestation <image uri> [--predicate-type]
cosign download attestation --platform linux/amd64 <image uri>
```

- `download signature`: signatures from the image, with registry auth/TLS flags and `--k8s-keychain` only.
- `download attestation`: in-toto attestations. Extra flags: `--predicate-type string` (only matching predicateType) and `--platform string` (for a specific platform image).

Use it to inspect what an attestation says before writing a Rego or CUE policy (see verify-attestation-policy).

Downloading is not verifying: treat the output as untrusted until `verify` or `verify-attestation` passes. `cosign tree <IMAGE>` shows what exists (see tree-artifacts); for SBOMs use attestations, not the deprecated `download sbom` (see download-sbom-deprecated).

The `--platform` value format is not shown on the page; check the help output.

## Checked

2026-11-04. Confirmed on the cosign download signature and download attestation reference pages: the two usage lines, the registry auth and TLS flags, `--k8s-keychain`, and `--predicate-type` and `--platform` on download attestation only. Removed: the use-case bullets about checking predicate types and debugging, and the guess at the platform format.

Method: documentation only; no commands were run.
