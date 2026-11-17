---
id: computing-software.messaging-and-integration.nats.username-password-and-bcrypt
name: username-password-and-bcrypt
category: computing-software
field: messaging-and-integration
product: nats
tags: [username-password, bcrypt, nats-server-passwd, authorization-users, config-reload]
level: practitioner
status: docs-checked
description: "Configure user/password auth in nats-server, store bcrypt hashes from nats server passwd, and reload without dropping clients."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/auth_intro/username_password.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: authenticate clients with usernames and passwords without storing plain-text secrets.

Single user:
```
authorization: { user: a, password: b }
```
or flags `nats-server --user a --pass b`.

Multiple users:
```
authorization: { users: [ {user: a, password: b}, {user: b, password: a} ] }
```

Bcrypt: generate a hash with the nats CLI, `nats server passwd`. It prompts twice for the password and prints a `$2a$...` string. Put that string, quoted, in place of the clear-text value: `{user: a, password: "<bcrypt-hash>"}`. The client still sends the clear password; the server compares against the hash.

Reload after adding or removing users, without restarting or disconnecting clients: `nats-server --signal reload`.

Gotchas: plain-text passwords in config or on the command line are visible to anyone who can read the file or process list; use bcrypt (and TLS so the password is not sent in clear). The password section only controls identity; permissions are a separate map covered by the authorization page.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
