---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.sbom-signing-and-attestation
name: sbom-signing-and-attestation
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [sbom-signing-and-attestation, sbom-distribution-and-integrity, sigstore, cosign, in-toto, attestation, slsa provenance, sign sbom, keyless signing, itam-licence-compliance]
level: advanced
status: docs-checked
description: "Sign SBOMs and attach in-toto attestations with Sigstore cosign so recipients can verify origin and integrity."
sources:
  - https://github.com/sigstore/cosign
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing SBOMs and attestations

Goal: trustworthy SBOM provenance.

Method:
- Sign an SBOM file with cosign sign-blob --bundle sbom.bundle sbom.json (--bundle writes everything needed to verify the blob; --key accepts a key file, KMS URI or Kubernetes secret).
- Attest to a container image: cosign attest --type spdxjson --predicate sbom.spdx.json <image@digest>.
- Consumers verify with cosign verify-attestation and expected identity/issuer.
- Pair with SLSA provenance describing the build.
- Store signatures with the release and publish the verification instructions.

Gotchas:
- Keyless identities must be pinned in verification policy.
- A signed SBOM proves origin, not accuracy.

Verify: verification succeeds from a clean environment.

## Checked

2026-11-02. Checked against the cosign command reference pages for sign-blob (--bundle, --key), attest (--predicate, --type values including spdxjson, cyclonedx, slsaprovenance) and verify-attestation (--certificate-identity, --certificate-oidc-issuer). Removed: the keyless OIDC wording (not on those pages).

Method: documentation only; no commands were run.
