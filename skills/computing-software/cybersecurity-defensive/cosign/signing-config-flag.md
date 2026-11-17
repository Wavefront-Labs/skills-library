---
id: computing-software.cybersecurity-defensive.cosign.signing-config-flag
name: signing-config-flag
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, signing-config, private-sigstore, custom-services]
level: advanced
status: docs-checked
description: "The --signing-config flag on cosign sign, sign-blob and attest-blob, its --bundle requirement for blobs, and the --trusted-root post-signing check."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign-blob.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest-blob.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Using a signing config

`--signing-config string` is listed on `cosign sign` ("path to a signing config file"), `cosign sign-blob` and `cosign attest-blob`. The pages do not describe the file's contents.

Rules from the flag text:
- On `sign-blob` and `attest-blob`: "Must provide --bundle, which will output verification material in the new format".
- `--trusted-root` is "optional path to a TrustedRoot JSON file to verify a signature after signing" (listed on sign, sign-blob and attest-blob).

## Checked

2026-11-04. Confirmed against the cosign sign, sign-blob and attest-blob docs: both flags and their exact help text on each command. Removed: the claim that the file selects Fulcio, Rekor, OIDC and TSA services instead of public-good defaults, the invented command examples, cross-references to signing-config-create, the `cosign trusted-root create` and `cosign verify --trusted-root` advice, and the claim about time-range versioning and rotation, none of which these pages state.
Method: documentation only; no commands were run.
