---
id: computing-software.cybersecurity-defensive.cosign.verify-attestation-policy
name: verify-attestation-policy
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, verify-attestation, policy, rego, cue, predicate-type]
level: advanced
status: docs-checked
description: "Verify image attestations and enforce Rego or CUE policies with cosign verify-attestation --type and --policy."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-attestation.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# verify-attestation with policy

```
cosign verify-attestation --key cosign.pub <IMAGE>
cosign verify-attestation --key cosign.pub --type <PREDICATE_TYPE> --policy <REGO_POLICY> <IMAGE>
cosign verify-attestation --key cosign.pub --type <PREDICATE_TYPE> --policy <CUE_POLICY> <IMAGE>
cosign verify-attestation --certificate-identity ... --certificate-oidc-issuer ... <IMAGE>
```

`--policy strings`: "specify CUE or Rego files with policies to be used for validation". The flag takes files.

How it fits:
- `--type` selects which attestations are checked (default `custom`), so pass the type you attested.
- The result is JSON by default (`-o text` available).
- Identity, issuer, GitHub claim, `--trusted-root`, `--use-signed-timestamps` and insecure flags behave as on `verify`.
- `--local-image` verifies one saved with `cosign save`.

Gotchas:
- The docs do not specify the input layout the policy sees; test policies against output of `cosign download attestation` and fail closed (deny unless the policy affirmatively passes).
- Without `--type`, you only validate against `custom` attestations.

## Checked

2026-11-04. Confirmed on the cosign verify-attestation reference page: the usage lines with Rego and CUE policies, `--policy` text, `--type` list with default custom, `-o` json or text, `--local-image`, the GitHub workflow flags and `--use-signed-timestamps`. Removed: the claim that the attestation subject must match the image digest (not on the page).

Method: documentation only; no commands were run.
