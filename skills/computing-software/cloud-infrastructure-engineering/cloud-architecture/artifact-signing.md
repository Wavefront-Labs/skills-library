---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.artifact-signing
name: artifact-signing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, artifact-signing, sbom, sigstore, cosign, slsa, provenance, admission-verification]
level: practitioner
status: draft
description: "Secure the software supply chain: generate SBOMs, sign images and attestations with Sigstore/cosign or Notation, record SLSA provenance and verify at deploy."
sources: ["https://docs.sigstore.dev/cosign/signing/overview/", "https://slsa.dev/spec/v1.0/", "https://notaryproject.dev/docs/", "https://www.cisa.gov/sbom"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SBOM and artefact signing

## Build side
1. **SBOM**: generate at build (Syft, Trivy, `docker buildx --sbom=true`) in SPDX or CycloneDX;
   attach to the image as an attestation.
2. **Provenance**: SLSA provenance from the CI system (GitHub Actions attestations, SLSA
   generators, Buildx `--provenance=mode=max`) showing source commit, builder and inputs.
3. **Sign**: `cosign sign --yes $IMAGE@sha256:...` keyless with OIDC identity (Fulcio certificate,
   Rekor transparency log) or with KMS keys (`--key awskms://...`); Notation with signing
   certificates in Key Vault / AWS Signer.
4. Always sign and deploy by **digest**, never by mutable tag.

## Deploy side
- Kubernetes admission: Sigstore policy-controller, Kyverno `verifyImages`, Ratify + Gatekeeper.
  Policy: image signed by our CI identity (issuer + subject regex) and has provenance from our repo.
- Cloud-native: GKE Binary Authorization, AWS Signer with ECS/EKS integrations, ACR + Notation.

## Steps
Start in audit mode, measure unsigned images, sign third-party base images you mirror, then enforce.

## Gotchas
- Verifying signature but not the signer identity (any valid Sigstore signature passes).
- SBOMs generated but never scanned or stored.

## Verify
- [ ] Unsigned image is rejected by admission in production.
- [ ] SBOM retrievable for every running image.
