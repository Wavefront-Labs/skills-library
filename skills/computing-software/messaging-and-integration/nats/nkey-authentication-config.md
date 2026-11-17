---
id: computing-software.messaging-and-integration.nats.nkey-authentication-config
name: nkey-authentication-config
category: computing-software
field: messaging-and-integration
product: nats
tags: [nkey, authorization-users, challenge-signing, server-config, sigcb]
level: practitioner
status: docs-checked
description: "Authorize users in nats-server by NKey public key and have clients sign the per-connection challenge with the seed."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/auth_intro/nkey_auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients with NKeys so the server never sees or stores a private key.

Mechanism: the server generates a random challenge on every connection; the client sends its public key and signs the challenge with its seed (private key). The docs call this an excellent replacement for token authentication, because the client must prove control of the private key.

Server side: generate a user key pair with the `nk` tool (`nk -gen user -pubout`): the line starting with `S` is the seed (secret), the one starting with `U` is the public key. Then configure only the public key:
```
authorization: {
  users: [
    { nkey: <user-public-key> }
  ]
}
```
No user, password or token property is needed; add `permission` sections as required.

Client side: give the client the public key and a signing callback that loads the seed safely (from a file or protected constant) and signs the nonce. The page's Node example passes `nkey: '<public key>'` and `sigCB: function (nonce) { ... return sk.sign(nonce); }`, using `nkeys.fromSeed` on the seed. Other languages expose an equivalent NKey option.

Gotchas: guard the seed like any secret; do not put it in config files that are committed.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
