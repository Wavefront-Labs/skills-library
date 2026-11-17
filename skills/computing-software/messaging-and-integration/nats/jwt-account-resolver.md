---
id: computing-software.messaging-and-integration.nats.jwt-account-resolver
name: jwt-account-resolver
category: computing-software
field: messaging-and-integration
product: nats
tags: [jwt, resolver, full-resolver, cache-resolver, resolver-preload, account-lookup]
level: practitioner
status: docs-checked
description: "Configure the built-in NATS account resolver (full vs cache), nsc push/pull, and the SYS claims update/lookup subjects."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/jwt/resolver.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let servers fetch account JWTs for decentralized auth.

Three resolver kinds: the NATS-based resolver (preferred default), `MEMORY` (accounts statically in config) and `URL` (your own account service). If the operator JWT already carries an account resolver URL, `resolver` is only needed to override it.

NATS-based resolver: built into nats-server, stores JWTs in a local directory (do not share one directory between servers). Admins manage JWTs with `nsc`, `nsc push` to servers, `nsc pull` to refresh the local copy.

`type: full` stores all JWTs and converges with peer resolvers eventually:
```
resolver: { type: full  dir: './jwt'  allow_delete: false  interval: "2m"  limit: 1000 }
```
With `allow_delete: true` a delete renames the file with a `.delete` suffix (rename it back and reload to restore; delete files manually to free space). `interval` is how often a server compares state with a random peer; `limit` rejects new JWTs past the cap. `resolver_preload` preloads JWTs, which can later be updated and survive restarts. Not every cluster server must be `full`.

`type: cache` keeps a subset with LRU eviction: `dir`, `limit` (evicts), `ttl: "2m"`. It fetches missing accounts from `full` resolvers and does not accept pushes from nsc, so it cannot run stand-alone.

Integration subjects via the system account: send a JWT to `$SYS.REQ.CLAIMS.UPDATE` to upload; subscribe to `$SYS.REQ.ACCOUNT.*.CLAIMS.LOOKUP` and reply with the JWT to implement your own account server.

Migration: `nsc pull` first, switch servers to the nats resolver, then point the operator's account server URL to the nats URLs.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
