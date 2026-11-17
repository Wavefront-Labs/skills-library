---
id: computing-software.cybersecurity-defensive.cosign.sbom-media-types
name: sbom-media-types
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, sbom-media-types, sbom-scope, spdx, cyclonedx, syft]
level: advanced
status: docs-checked
description: "The deprecated cosign SBOM attachment layout: layer media types for SPDX, CycloneDX and syft, plus the dev.sigstore.sbom.scope annotation values."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SBOM_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SBOM attachment spec (deprecated)

Warning in the spec: SBOM attachments are deprecated and support will be removed in a Cosign release soon after 2024-02-22; use SBOM attestations (ATTESTATION_SPEC) instead.

Layout: an OCI Image Manifest V1. Each individual SBOM is a `layer` with a standard descriptor; the `layers` list is ordered, but no order is assumed or important. Multiple SBOMs in multiple formats may be attached to one image, and the descriptor's `mediaType` describes the format.

Media types:
- `application/vnd.cyclonedx` (format suffixes such as `+xml` and `+json` are allowed)
- `text/spdx` (suffixes such as `text/spdx+xml` and `text/spdx+json`)
- `application/vnd.syft+json` (syft is a JSON-only format)

Scope annotation on the descriptor, key `dev.sigstore.sbom.scope`:
- `all`: the whole object; a descriptor with no scope is assumed to be the same as `all`
- `layer=sha256:$DIGEST`: the layer with that digest
- `path=<foo>`: the file at path `foo` in the flattened image
- Scopes may be repeated, separated by `,`: `layer=sha256:$DIGEST,layer=sha256:$OTHERDIGEST`

The spec does not specify how clients should behave when multiple SBOMs are present (clients may list them all or filter by type or scope). It says the "relationship" of an SBOM that describes the build environment rather than the object's contents will be tracked by the spec "somehow", but it is not yet decided how.

Instead of attachments, the `cosign attest` docs list `spdx`, `spdxjson` and `cyclonedx` among the values for `--type`.

## Checked

2026-11-04. Confirmed against the cosign specs page SBOM_SPEC and the cosign_attest docs page: deprecation warning and date, manifest layout, media types and suffixes, scope annotation key and values, multiple-SBOM client behaviour, relationship note, `--type` values. Removed: the statement that an attached SBOM is not a signed statement (not on the page) and the pointer to a `download-sbom-deprecated` skill.
Method: documentation only; no commands were run.
