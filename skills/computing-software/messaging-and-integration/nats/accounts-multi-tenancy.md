---
id: computing-software.messaging-and-integration.nats.accounts-multi-tenancy
name: accounts-multi-tenancy
category: computing-software
field: messaging-and-integration
product: nats
tags: [accounts, multi-tenancy, exports, imports, service-import, stream-export]
level: practitioner
status: docs-checked
description: "Isolate tenants with NATS accounts and share data using stream/service exports and imports, with prefix and to remapping."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/accounts.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split a server into isolated messaging contexts and share only what you choose.

Accounts live in the `accounts` map keyed by account name. Each has `users` (same user maps as elsewhere: password, nkey, permissions), `exports` and `imports`. Users in different accounts cannot see each other's messages; the subject space is not globally shared. Think of one account as the messaging container for one application.

Exports: `stream` (a subject the account publishes) or `service` (a subject the account subscribes to and answers), mutually exclusive; optional `accounts` list restricts importers (omitted means public); `response_type` is `single` (default) or `stream`. Note that "stream" here means a core message stream, not a JetStream stream.

Imports: `stream` or `service` with a source map `{account: A, subject: ...}`; `prefix` remaps a stream locally; `to` remaps a service locally (service imports cannot use wildcards).

Example from the page: account A exports `{stream: puba.>}`, `{service: pubq.>}`, `{stream: b.>, accounts: [B]}`, `{service: q.b, accounts: [B]}`; B imports `{stream: {account: A, subject: b.>}}` and `{service: {account: A, subject: q.b}}`; C imports `{stream: {account: A, subject: puba.>}, prefix: from_a}` so it receives `from_a.puba.>`, and `{service: {account: A, subject: pubq.C}, to: Q}`.

Gotchas: a public service is usable by anyone who knows the full subject; make sensitive exports private by listing `accounts`.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
