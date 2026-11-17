---
id: computing-software.messaging-and-integration.nats.nk-keys-and-nkey-auth
name: nk-keys-and-nkey-auth
category: computing-software
field: messaging-and-integration
product: nats
tags: [nkeys, nk, ed25519, seed, public-key, nkey-auth]
level: practitioner
status: docs-checked
description: "Generate Ed25519 NKeys with the nk tool and configure a server user by public key; seeds are secrets."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/nats-tools/nk.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: generate an NKey pair and authorize it on a server without storing a secret there.

NKeys are an Ed25519 public-key signature scheme. The server sends a challenge; the client presents its public key and signs the challenge with its private key, so the server verifies identity but never holds secrets. The docs describe it as a strong replacement for token authentication.

Install: `go install github.com/nats-io/nkeys/nk@latest`.

Generate a user key and print the public key too: `nk -gen user -pubout`. Two lines come out:
- the seed, starting with `S` (second letter `U` for user): the private key, treat as a secret;
- the public key, starting with `U`: safe to share.

Server config uses only the public key:
```
authorization: {
  users: [
    { nkey: <user-public-key> }
  ]
}
```
No other user property is required. The client is configured with the seed (private key) via its NKey option, as described on the nkey authentication page.

Gotchas: never commit or log the seed; the prefix letters tell you the key type (S seed, U user public). Account and operator keys are managed with nsc rather than nk when using JWT auth.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
