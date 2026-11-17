---
id: computing-software.cybersecurity-defensive.cosign.download-sbom-deprecated
name: download-sbom-deprecated
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, download-sbom, sbom-deprecated, sbom-attestation]
level: practitioner
status: docs-checked
description: "The deprecated cosign download sbom and SBOM attachments, their removal warning, and the replacement: SBOM attestations with spdx or cyclonedx types."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_download_sbom.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/SBOM_SPEC.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deprecated SBOM attachments

`cosign download sbom <image uri>` is marked DEPRECATED. The warning: "SBOM attachments are deprecated and support will be removed in a Cosign release soon after 2024-02-22 (see https://github.com/sigstore/cosign/issues/2755). Instead, please use SBOM attestations."

It supports `--platform` for a specific platform image plus registry flags.

Migrate:

```
cosign attest --type spdxjson --predicate sbom.spdx.json --key cosign.key <IMAGE DIGEST>
cosign verify-attestation --type spdxjson --key cosign.pub <IMAGE>
cosign download attestation --predicate-type <type> <IMAGE>
```

Valid SBOM-related `--type` values: `spdx`, `spdxjson`, `cyclonedx` (see attest-predicate-types).

Related cleanup: `cosign clean --type sbom` is also marked deprecated.

Why attestations: the attestation spec serializes attestations as DSSE envelopes, whereas an attached SBOM is a layer in an SBOM manifest (see sbom-media-types).

If a pipeline still downloads attached SBOMs, check your cosign version; the warning says support will be removed.

## Checked

2026-11-04. Confirmed on the cosign download sbom page (deprecation text, issue link, `--platform`), the clean page (`--type` accepts sbom, marked deprecated), the attest and verify-attestation pages (`--type` values spdx, spdxjson, cyclonedx), the SBOM spec (layer-based layout) and the attestation spec (DSSE envelope). Removed: the claim that attestations are verifiable with policy in contrast to attachments.

Method: documentation only; no commands were run.
