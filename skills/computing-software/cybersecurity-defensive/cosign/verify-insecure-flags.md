---
id: computing-software.cybersecurity-defensive.cosign.verify-insecure-flags
name: verify-insecure-flags
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, insecure-ignore-tlog, insecure-ignore-sct, check-claims, verification-bypass]
level: advanced
status: docs-checked
description: "What cosign verify --insecure-ignore-tlog, --insecure-ignore-sct and --check-claims=false skip, when they are justified and what you lose."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify-blob-attestation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relaxing verification

Three flags weaken checks. Treat each as a documented exception.

- `--insecure-ignore-tlog`: skip transparency log verification, "to be used when an artifact signature has not been uploaded to the transparency log. Artifacts cannot be publicly verified when not included in a log". The sign page has an example with `--tlog-upload=false`.
- `--insecure-ignore-sct`: do not check that the certificate embeds an SCT, a proof of inclusion in a certificate transparency log.
- `--check-claims` (default true): whether to check the claims found. Setting `--check-claims=false` skips that check, so use it only for inspection.

On `verify-blob-attestation`, `--check-claims=false` means "only the DSSE envelope is verified" and the in-toto subject digest is not compared.

Rules of thumb:
- Treat `--insecure-ignore-tlog` as a last resort: it disables the transparency log check.
- Record why the flag is used in the pipeline; a green check with these flags is a weaker statement.

## Checked

2026-11-04. Confirmed on the cosign verify, verify-blob-attestation and sign reference pages: the quoted text for `--insecure-ignore-tlog`, the description of `--insecure-ignore-sct`, `--check-claims` default true, the verify-blob-attestation text "only the DSSE envelope is verified", and the `--tlog-upload=false` example. Removed: the claim that check-claims=false drops the image digest binding on verify, and the legitimate-case remark (neither is on the pages).

Method: documentation only; no commands were run.
