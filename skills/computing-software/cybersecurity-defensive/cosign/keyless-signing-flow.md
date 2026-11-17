---
id: computing-software.cybersecurity-defensive.cosign.keyless-signing-flow
name: keyless-signing-flow
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, keyless, oidc-provider, fulcio-auth-flow, fulcio, rekor, oidc]
level: practitioner
status: docs-checked
description: "How cosign keyless signing works and the flags that steer it: --oidc-provider, --fulcio-auth-flow, OIDC client id, redirect URL and disabling ambient providers."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keyless signing flow

`cosign sign <IMAGE DIGEST>` with no `--key` does: ephemeral keys, OIDC login, Fulcio certificate whose subject matches the identity (for example the login email), Rekor entry, then upload of signature and certificate to the registry.

Flags:
- `--oidc-provider` picks the token source. If unset, all are tried. Options: spiffe, google, github-actions, filesystem, buildkite-agent.
- `--oidc-disable-ambient-providers` stops cosign reading ambient credentials.
- `--fulcio-auth-flow` chooses the interactive flow: normal, device, token or client_credentials. By default it is chosen from the runtime environment.
- `--oidc-client-id` (default `sigstore`), `--oidc-client-secret-file`, `--oidc-redirect-url` (default `http://localhost:0/auth/callback`).
- `-y` skips the prompt that warns the identity is stored permanently in public logs.

Gotchas:
- The same flags exist on `sign-blob` and `attest`.
- Consumers must verify with an expected identity and issuer (see verify-keyless-identity); a bare `cosign verify` is not enough.
- Signing depends on several services; the README advises retrying on HTTP errors.

## Checked

2026-11-08. Read in full: the `cosign sign` reference, `cosign verify` reference and the cosign README (raw, sigstore/cosign). Confirmed the flow, flag names, defaults, the confirmation prompt and the retry advice. Removed the unsourced remark that headless shells suit `device`.

Method: documentation only; no commands were run.
