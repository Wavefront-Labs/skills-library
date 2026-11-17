---
id: computing-software.cybersecurity-defensive.cosign.attestation-oci-layout
name: attestation-oci-layout
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, attestation-layout, dsse, in-toto, subject-verification]
level: sme
status: docs-checked
description: "How cosign lays out in-toto attestations in an OCI image manifest as DSSE layers, and the subject verification rule for implementers."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/ATTESTATION_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-attestation.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_download_attestation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attestation layout (spec)

An attestation object is an OCI Image Manifest V1. Each attestation is one `layer` with a standard descriptor. Layer order is not significant. Several attestations may be attached to one image.

Format: in-toto Attestation serialized as a DSSE envelope, layer media type `application/vnd.dsse.envelope.v1+json`. Other formats may be used if `mediaType` describes them, but implementations may not understand them.

Example descriptor fields: `mediaType`, `size`, `digest` (sha256).

Subject verification:
- Attestations MAY refer to multiple subjects, the whole image or a part.
- Implementations MUST verify the relationship between the statement `subject` and the container image.
- Implementations MUST support attestations that reference the entire image; other relationships are optional.

Practical check: use `cosign verify-attestation` (it checks claims by default; `--check-claims=false` disables that, see verify-insecure-flags) and read the real subject digest with `cosign download attestation <IMAGE>`.

## Checked

2026-11-08. Read in full: ATTESTATION_SPEC.md (raw, sigstore/cosign), the `cosign download attestation` reference and the first 80 lines of the `cosign verify-attestation` reference (synopsis, examples and the options up to `--policy`; `--check-claims` default true confirmed). Confirmed the manifest layout, media type, layer ordering and the subject verification rules. Removed the unsourced sentence about the legacy `.att` tag and OCI 1.1 referrers.

Method: documentation only; no commands were run.
