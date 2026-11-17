---
id: computing-software.cloud-infrastructure-engineering.hashicorp-vault.vault-generate-root-token
name: vault-generate-root-token
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-vault
tags: [vault, generate-root, root-token, break-glass]
level: practitioner
status: docs-checked
description: "Create a short-lived root token with operator generate-root using an OTP or PGP key, then revoke it after the emergency task."
sources: ["https://developer.hashicorp.com/vault/docs/commands/operator/generate-root", "https://developer.hashicorp.com/vault/docs/concepts/tokens"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Revoke the initial root token after setup and generate a new one only for break-glass tasks. The process needs a quorum of unseal (or recovery) keys.

```sh
vault operator generate-root -generate-otp         # prints an OTP
vault operator generate-root -init -otp=<otp>      # starts generation
vault operator generate-root                       # enter each share; repeat to threshold
vault operator generate-root -decode=<encoded-token> -otp=<otp>
vault token revoke <root-token>
vault operator generate-root -cancel               # reset an unfinished attempt
```

Use `-pgp-key` instead of the OTP to receive the token encrypted to a public key. `-status` checks progress; `-dr-token` and `-recovery-token` produce those token types.

Gotchas: the nonce supplied at init must go with every share, and a mismatch breaks the process. Only one generation can be in progress. Root tokens can be set to never expire and carry the `root` policy, so revoke the token as soon as the task is done. Prefer a time-limited, policy-scoped admin token for daily operations.

## Checked

2026-11-03. Confirmed against the `operator generate-root` command page (flags `-init`, `-otp`, `-generate-otp`, `-decode`, `-nonce`, `-pgp-key`, `-status`, `-cancel`, `-dr-token`, `-recovery-token`; one OTP or PGP key must be provided to start; only one attempt at a time) and the Vault tokens concepts page (root tokens, never expire). Removed: claim that `-init` prints the OTP, calendar-reminder advice and an invented verify step.

Method: documentation only; no commands were run.
