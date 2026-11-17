---
id: computing-software.messaging-and-integration.nats.nsc-revocation
name: nsc-revocation
category: computing-software
field: messaging-and-integration
product: nats
tags: [revocation, nsc-revocations, activation, account-jwt, revoke-user]
level: practitioner
status: docs-checked
description: "Revoke NATS users and export activations with nsc revocations: time-based semantics, --at, push to servers, and permanent delete risk."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/nats-tools/nsc/revocation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: cut off a user or an export activation without rotating the account key.

Two revocation kinds live in the Account JWT so servers can enforce them: users (by public key) and activations (an account's access to an export). Revocation is time-based: revoking at time T invalidates every user JWT or activation token created before T; tokens issued after T work again. That lets the account owner reissue a corrected JWT after revoking.

Commands (`nsc revocations -h`): `add-user`, `add_activation`, `delete-user`, `delete_activation`, `list-users`, `list_activations`. Both add commands accept `--at` as a unix timestamp; default is now, and you can set it in the past when you know when a key was compromised. The global `-K` / `--private-key` flag supplies a signing key.

Rollout: with the built-in NATS resolver you must push the updated account, for example `nsc push -i` or `nsc push -a B -u nats://localhost`. Connected clients whose user was revoked are disconnected immediately after the push.

Gotchas: deleting a revocation is permanent and can make an old user JWT or activation valid again, so delete only when the tokens have expired.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
