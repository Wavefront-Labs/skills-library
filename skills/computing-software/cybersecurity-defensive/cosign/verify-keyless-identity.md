---
id: computing-software.cybersecurity-defensive.cosign.verify-keyless-identity
name: verify-keyless-identity
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, certificate-identity, certificate-oidc-issuer, identity-regexp, issuer-regexp, keyless]
level: practitioner
status: docs-checked
description: "Verify keyless signatures by pinning the expected Fulcio certificate identity and OIDC issuer, exact or regexp, and why both are mandatory."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyless verification: identity and issuer

```
cosign verify $IMAGE \
  --certificate-identity=$IDENTITY \
  --certificate-oidc-issuer=$OIDC_ISSUER
```

Both are required: "Either --certificate-identity or --certificate-identity-regexp must be set for keyless flows", and likewise for the issuer (`--certificate-oidc-issuer` or `--certificate-oidc-issuer-regexp`).

- Identity values "include email address, DNS names, IP addresses, and URIs".
- Issuer examples from the help: `https://token.actions.githubusercontent.com`, `https://oauth2.sigstore.dev/auth`.
- Regexp flags accept the Go RE2 syntax.

GitHub Actions blob example from the README:
`--certificate-identity "https://github.com/ORG/REPO/.github/workflows/release.yml@refs/heads/main"` with issuer `https://token.actions.githubusercontent.com`.

Same flags exist on `verify-attestation`, `verify-blob` and `verify-blob-attestation`.

If the signature was made with a key, use `--key` instead; these flags apply to certificate-based signatures.

## Checked

2026-11-04. Confirmed on the cosign verify, verify-blob and verify-blob-attestation reference pages and in the README: the two required flags and their regexp alternatives (identity: email, DNS names, IP addresses, URIs; issuer examples), Go RE2 syntax, and the GitHub Actions blob example. Removed: the claim about unanchored patterns matching attacker-controlled identities (not on the pages).

Method: documentation only; no commands were run.
