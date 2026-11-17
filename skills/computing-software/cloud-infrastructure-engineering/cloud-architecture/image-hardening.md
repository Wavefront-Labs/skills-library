---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.image-hardening
name: image-hardening
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, infrastructure-protection, image-hardening, golden-images, software-supply-chain, distroless, image-signing, cosign, sbom, admission-control, slsa]
level: advanced
status: draft
description: "Harden VM and container images and the supply chain feeding them: golden image pipelines, minimal bases, SBOMs, signing and verification at admission, and rebuild cadence."
sources: ["https://slsa.dev/spec/v1.0/", "https://docs.sigstore.dev/cosign/signing/overview/", "https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html", "https://kubernetes.io/docs/concepts/security/pod-security-standards/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image and software supply chain hardening

## VM images
1. Golden image pipeline: Packer / EC2 Image Builder / Azure Image Builder / GCE image pipelines,
   applying CIS hardening, agents (monitoring, security), patches.
2. Scan before publishing (Inspector, Defender, OS scanners); version and share images to accounts.
3. Rebuild on a cadence (e.g. monthly + on critical CVEs) and replace instances (immutable) rather than patching in place.
4. Restrict which images can launch (AWS "allowed AMIs" account setting, Azure Policy allowed images, GCP `compute.trustedImageProjects` org policy).

## Container images
1. Minimal bases (distroless, Chainguard/Wolfi, Alpine/slim), non-root user, no shell where possible.
2. Pin base images by digest; automated rebuilds on base updates (Renovate/Dependabot).
3. **SBOM** at build (Syft, `docker buildx --sbom`), vulnerability scan (Trivy, Grype, registry scanning).
4. **Sign** images and attestations (cosign keyless via OIDC; Notation); generate SLSA provenance
   (e.g. GitHub artifact attestations / slsa-github-generator).
5. **Verify at deploy**: admission policies (Kyverno `verifyImages`, Sigstore policy-controller,
   GKE Binary Authorization, AKS image integrity) allowing only signed images from trusted registries.
6. Runtime: Pod Security Standards `restricted`, read-only root filesystem, dropped capabilities.

## Verify
- [ ] Unsigned image deploy is rejected in prod clusters.
- [ ] Every running image has an SBOM and scan result; criticals have SLA.
