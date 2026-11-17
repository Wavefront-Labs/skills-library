---
id: computing-software.cloud-infrastructure-engineering.kubernetes.sbom-attestations-cosign-oras
name: sbom-attestations-cosign-oras
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, supply-chain, sbom-attestation, oras, cosign, syft]
level: practitioner
status: docs-checked
description: "Generate SBOMs for images and attach them as signed cosign attestations or OCI referrers with oras, then discover and verify them from the registry."
sources: ["https://docs.sigstore.dev/cosign/verifying/attestation/", "https://oras.land/docs/commands/oras_attach", "https://github.com/anchore/syft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attaching SBOMs to images

## Generate
```bash
syft registry.internal/app@sha256:<digest> -o cyclonedx-json > sbom.cdx.json
# or at build time with BuildKit
docker buildx build --sbom=true --provenance=mode=max -t registry.internal/app:1.4 --push .
```

## Option A: signed attestation (cosign)
```bash
cosign attest --yes --key cosign.key --type cyclonedx --predicate sbom.cdx.json registry.internal/app@sha256:<digest>
cosign verify-attestation --key cosign.pub --type cyclonedx registry.internal/app@sha256:<digest> \
  | jq -r .payload | base64 -d | jq .predicateType
```
The SBOM is wrapped in an in-toto statement and signed, so admission can require it
(Kyverno `verifyImages.attestations`, or `ImageValidatingPolicy` `attestations`; the ClusterPolicy form is deprecated as of Kyverno v1.19).

## Option B: OCI referrer (oras)
```bash
oras attach --artifact-type application/vnd.cyclonedx+json registry.internal/app@sha256:<digest> sbom.cdx.json
oras discover registry.internal/app@sha256:<digest>      # tree view is the default
oras pull registry.internal/app@sha256:<sbom-manifest-digest> -o ./sboms
```
Referrers are linked to the image digest through the OCI 1.1 referrers API (or the tag-schema
fallback on older registries). Unsigned unless you also sign the referrer manifest.

## Choosing
- Need a verifiable claim at admission: cosign attestation.
- Need tools (scanners, Dependency-Track) to discover SBOMs generally: OCI referrers. Many teams do both.

## Gotchas
- Always reference by digest; a tag can move and leave the SBOM pointing at a different image.
- Registry support for the referrers API varies; `oras` falls back to the referrers tag scheme (`--distribution-spec v1.1-referrers-tag`).
- Copying images between registries must copy referrers too (`oras cp -r` copies an artifact and its referrers).

## Checked

Checked 2026-10-27 against the oras docs source (oras-project/oras-www, v1.3 command pages), the cosign CLI reference, the Syft README and the Docker build attestation docs.

- `oras attach --artifact-type`, `oras discover` (tree is the default format, `-o` is deprecated), `oras pull -o <dir>`, `oras cp -r` copying referrers, and `--distribution-spec v1.1-referrers-api|v1.1-referrers-tag` confirmed.
- cosign `attest` / `verify-attestation` with `--type cyclonedx` (listed among the predicate types) and the in-toto payload shape (`jq -r .payload | base64 -d`, `predicateType`) confirmed.
- `syft <image> -o cyclonedx-json` confirmed; `docker buildx build --sbom=true --provenance=mode=max` confirmed in the Docker docs.
- Removed unconfirmed claims: the `.predicate.components` jq path, named registries supporting referrers, and `crane` referrers support.

Method: documentation only; no commands were run.
