---
id: computing-software.cybersecurity-defensive.cosign.attest-predicate
name: attest-predicate
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, attest, predicate, no-upload, in-toto, dsse]
level: practitioner
status: docs-checked
description: "Create and attach a signed in-toto attestation to an image with cosign attest --predicate, from a file or stdin, or print it with --no-upload."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cosign attest

```
cosign attest --predicate <FILE> --type <TYPE> --key cosign.key <IMAGE DIGEST>
cosign attest --timeout 90s --predicate <FILE> --type <TYPE> <IMAGE>    # keyless
echo <PAYLOAD> | cosign attest --predicate - <IMAGE>                    # stdin
cosign attest --predicate <FILE> --type <TYPE> --key cosign.key --no-upload true <IMAGE>
```

- `--predicate`: path to the predicate file (or `-`).
- `--type`: predicate type; default `custom`. See attest-predicate-types.
- `--no-upload`: do not upload; "send the attestation output to STDOUT".
- `--statement`: path to a full in-toto statement file.
- `--bundle`: write verification material to a file.
- Key sources, certificate flags, KMS URIs, registry flags work as on `sign`.

Payloads are signed with DSSE. The README: "All of the standard key management systems are supported."

Verify with `cosign verify-attestation` (see verify-attestation-policy). The README says to sign images by digest (`@sha256:...`).

Legacy registries: set `COSIGN_DOCKER_MEDIA_TYPES=1` (see docker-media-types-legacy).

## Checked

2026-11-04. Confirmed on the cosign attest reference page (examples for key, keyless with `--timeout 90s`, stdin, `--no-upload`, COSIGN_DOCKER_MEDIA_TYPES; flags `--predicate`, `--type` default custom, `--statement`, `--bundle`, registry and certificate flags) and in the README (DSSE signing, all standard key management systems supported, sign by digest). Removed: the claim about the statement subject.

Method: documentation only; no commands were run.
