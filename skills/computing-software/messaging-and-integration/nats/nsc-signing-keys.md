---
id: computing-software.messaging-and-integration.nats.nsc-signing-keys
name: nsc-signing-keys
category: computing-software
field: messaging-and-integration
product: nats
tags: [signing-keys, nkeys, key-rotation, nsc-generate-nkey, operator-signing-key]
level: practitioner
status: docs-checked
description: "Protect identity keys with nsc signing keys: generate with nsc generate nkey, add with --sk, sign with -K, and rotate on compromise."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/nats-tools/nsc/signing_keys.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep operator and account identity keys offline and sign day-to-day with replaceable signing keys.

Signing keys are extra NKEY identities of the same kind (operator or account) that are listed in the JWT and carry the same trust as the issuer key. A JWT is valid if signed by the issuer or by a listed signing key. If a signing key leaks, remove it from the entity, add a new one and reissue; JWTs signed by the removed key then stop validating. This is a blunt tool, so use several signing keys and rotate them to limit the blast radius.

Workflow from the page:
1. `nsc add operator O2`.
2. `nsc generate nkey --operator --store` prints the seed (starts with `S`) and the public key (starts with `O`) and stores the key file under the nkeys directory.
3. `nsc edit operator --sk <operator-public-key>` adds it as a signing key.
4. Create an account the same way (account nkey, then `nsc edit account --sk ...`), sign accounts with the operator signing key, and users with the account signing key.

All signing-key operations use the global flag `-K` / `--private-key`: whenever you modify an entity you must supply the parent key that signs the JWT; normally this is automatic, but with signing keys you pass it explicitly.

Gotchas: `nsc` does not track the public or private signing keys for you, so you must store and manage them yourself; in production keep seeds in secured files and reference them from there.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
