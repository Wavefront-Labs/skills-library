---
id: computing-software.cybersecurity-defensive.cosign.generic-predicate-spec
name: generic-predicate-spec
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, generic-predicate, custom-predicate, in-toto-statement]
level: advanced
status: docs-checked
description: "The cosign generic predicate used by --type custom: base64 data plus an RFC 3339 UTC timestamp wrapped in an in-toto Statement."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/specs/COSIGN_PREDICATE_SPEC.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic predicate

Cosign supports in-toto attestations using the predicate model. Several well-known predicates are supported natively; the generic predicate is a simple format for data that does not fit other types.

- `data`: raw data to place in the attestation, a base64-encoded string of bytes
- `timestamp`: when the attestation was generated, RFC 3339, UTC timezone

Example statement from the spec (an attestation containing a data file containing `foo`):

```
{"_type":"https://in-toto.io/Statement/v0.1",
 "predicateType":"https://cosign.sigstore.dev/attestation/v1",
 "subject":[{"name":"...","digest":{"sha256":"..."}}],
 "predicate":{"Data":"foo\n","Timestamp":"2021-08-11T14:51:09Z"}}
```

Notes:
- The spec's prose says `data` is base64-encoded, while its example shows `Data` as plain `foo\n` (capitalised `Data` and `Timestamp` keys in the example).
- The predicateType shown in the example is `https://cosign.sigstore.dev/attestation/v1`.
- `cosign attest --predicate <FILE> --type <TYPE> <IMAGE>`: the `--type` flag accepts slsaprovenance, slsaprovenance02, slsaprovenance1, link, spdx, spdxjson, cyclonedx, vuln, openvex, custom or a URI; the default is `custom`.

## Checked

2026-11-04. Confirmed against the cosign specs page COSIGN_PREDICATE_SPEC and the cosign_attest docs page: field definitions, example statement, `--type` values and `custom` default. Removed: the instruction to inspect output with `cosign download attestation`, the `cosign verify-attestation --type custom` line (neither page documents it), and the generic advice to prefer typed predicates.
Method: documentation only; no commands were run.
