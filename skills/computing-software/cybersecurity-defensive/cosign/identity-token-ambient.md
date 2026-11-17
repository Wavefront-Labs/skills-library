---
id: computing-software.cybersecurity-defensive.cosign.identity-token-ambient
name: identity-token-ambient
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, identity-token, ambient-credentials, ci, oidc]
level: practitioner
status: docs-checked
description: "Supply an OIDC identity token to cosign directly with --identity-token (value or file) or rely on ambient CI credentials, and when to disable ambient providers."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign-blob.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_verify.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity tokens and ambient credentials

`--identity-token string`: the identity token used to get a certificate from Fulcio. "the token or a path to a file containing the token is accepted."

```
cosign sign --identity-token /path/to/token --yes <IMAGE DIGEST>
```

Use it when the token comes from your own system and no browser flow is possible.

Ambient credentials: when `--oidc-provider` is unset, cosign tries all providers (spiffe, google, github-actions, filesystem, buildkite-agent).

Control:
- `--oidc-provider github-actions` pins one source.
- `--oidc-disable-ambient-providers` ("ambient credentials will not be read") stops cosign reading ambient credentials.

The same flags are on `sign`, `sign-blob`, `attest` and `attest-blob`.

## Checked

2026-11-08. Read in full: the `cosign sign`, `cosign sign-blob` and `cosign verify` references; the flag lines of the `cosign attest` and `cosign attest-blob` references were matched by search. Confirmed the flag wording, provider list, and the issuer example. Removed the unsourced claims about workload identity needing no flags and about forcing the interactive flow.

Method: documentation only; no commands were run.

Verification side: the Fulcio certificate records the issuer, so verifiers pass `--certificate-oidc-issuer` that matches your token issuer (for GitHub Actions the docs example is `https://token.actions.githubusercontent.com`).
