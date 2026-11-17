---
id: computing-software.messaging-and-integration.nats.nsc-operator-account-user
name: nsc-operator-account-user
category: computing-software
field: messaging-and-integration
product: nats
tags: [nsc, operator, account, user, jwt, nats-resolver, nsc-push]
level: practitioner
status: docs-checked
description: "Bootstrap decentralized JWT auth with nsc: add operator/account/user, generate resolver config, set system account, push, set user permissions."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/using-nats/nats-tools/nsc/basics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: create the operator, account and user JWT chain with `nsc` and get a server to accept it.

Commands from the page:
- `nsc add operator MyOperator`, then `nsc edit operator --service-url nats://localhost:4222`.
- `nsc add account MyAccount`, `nsc add user MyUser`.
- Inspect: `nsc list keys` (add `--show-seeds` only on a trusted terminal), `nsc describe operator|account|user MyUser`, `nsc env`.
- Server config for the built-in resolver: `nsc generate config --nats-resolver > resolver.conf`. This requires a system account: `nsc add account -n SYS` then `nsc edit operator --system-account SYS`.
- Publish account JWT changes to a running server: `nsc push -a MyAccount -u nats://localhost`.
- Smoke test using embedded tooling: `nsc sub --user MyUser ">"` and `nsc pub --user MyUser hello NATS`; a `nats` context can also be created.
- Permissions per user: `nsc add user s --allow-pub "_INBOX.>" --allow-sub q` (service) and `nsc add user c --allow-pub q --allow-sub "_INBOX.>"` (client); check with `nsc describe user s`.

Assets: the nsc stores directory holds JWTs; the NKEYS directory holds private keys, which must be protected and backed up. The operator JWT goes into the server config; the account and user JWTs are what servers and clients exchange.

Gotcha: changes made locally to an account do nothing on a server using the NATS resolver until you `nsc push` them.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
