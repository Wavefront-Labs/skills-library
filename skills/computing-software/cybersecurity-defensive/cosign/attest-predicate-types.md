---
id: computing-software.cybersecurity-defensive.cosign.attest-predicate-types
name: attest-predicate-types
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, predicate-type, slsa-provenance, openvex, spdx, cyclonedx, vuln]
level: practitioner
status: docs-checked
description: "Choose the --type for cosign attest and verify-attestation: slsaprovenance variants, link, spdx, spdxjson, cyclonedx, vuln, openvex, custom or a URI."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-attestation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Predicate types

`--type` accepts one of: `slsaprovenance`, `slsaprovenance02`, `slsaprovenance1`, `link`, `spdx`, `spdxjson`, `cyclonedx`, `vuln`, `openvex`, `custom` (default), or a URI.

```
cosign attest --type cyclonedx --predicate sbom.cdx.json --key cosign.key <IMAGE DIGEST>
cosign attest --type https://example.com/my-predicate/v1 --predicate p.json <IMAGE DIGEST>
```

The same list applies to `attest-blob`, `verify-attestation` and `verify-blob-attestation`.

Guidance:
- SBOMs: the deprecated attach path is replaced by SBOM attestations (`spdx`, `spdxjson`, `cyclonedx`).
- `vuln` follows cosign's vulnerability scan record (see vuln-attestation-spec); `custom` wraps raw data (see generic-predicate-spec).
- Filter downloads with `cosign download attestation --predicate-type`.
- The bundle annotation `dev.sigstore.bundle.predicateType` can reflect the predicate of a DSSE-wrapped in-toto statement (bundle spec).

The pages do not map each short name to its predicateType URI; read it from the downloaded attestation.

## Checked

2026-11-04. Confirmed on the cosign attest, attest-blob, verify-attestation and verify-blob-attestation reference pages (the `--type` list and default custom), the vulnerability attestation spec (predicateType https://cosign.sigstore.dev/attestation/vuln/v1) and the bundle spec annotation. Removed: the advice that the verify type must equal the attest type.

Method: documentation only; no commands were run.
