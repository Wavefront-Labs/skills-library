---
id: computing-software.messaging-and-integration.nats.auth-callout-setup
name: auth-callout-setup
category: computing-software
field: messaging-and-integration
product: nats
tags: [auth-callout, external-auth, issuer, xkey, auth-users, iam]
level: practitioner
status: docs-checked
description: "Delegate NATS authentication to your own service with auth_callout: issuer NKey, auth_users, account, xkey encryption and migration care."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/auth_callout.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let an application service decide who connects and with which permissions (LDAP, OAuth, a database), available from NATS 2.10.0.

Three phases, in this order: implement the auth service, plan migration, then enable configuration. Enabling config before the service is deployed can lock out existing systems.

Service: it handles authorization request claims and returns authorization response claims containing user claims; Go support is in the nats-io/jwt v2 package. See the NATS By Example auth callout sample for a reference implementation.

Migration (centralized/config-file model): existing config users are ignored once callout is on, so the service must authenticate everyone, assign accounts and permissions, including the system account user(s) and the implicit no-auth user. Port users first.

Config goes in `authorization { auth_callout { ... } }`:
- `issuer`: public key of the NKey that signs authorization payloads (generate with `nsc generate nkey --account`);
- `auth_users`: users (or nkeys) in `account` that are the callout service identities;
- `account`: where those users live (default `$G`);
- `xkey`: optional x25519 public key to encrypt request payloads; recommended (generate with `nsc generate nkey --curve`).

Minimal: `authorization { users: [ { user: auth, password: <secret> } ]  auth_callout { issuer: <public key>  auth_users: [ auth ] } }`.

For new setups use explicit accounts: `AUTH` (callout users), `APP`, and `SYS` with `system_account: SYS`. When migrating a multi-account system keep `accounts` but drop their `users`.

Gotchas: generate your own keys; keep seeds secret.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
