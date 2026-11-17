---
id: computing-software.messaging-and-integration.nats.subject-permissions
name: subject-permissions
category: computing-software
field: messaging-and-integration
product: nats
tags: [authorization, permissions, publish-subscribe, allow-responses, default-permissions, inbox]
level: practitioner
status: docs-checked
description: "Restrict users by subject with publish/subscribe allow and deny lists, default_permissions, queue permissions and allow_responses."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/securing_nats/authorization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: limit which subjects each authenticated user may publish and subscribe to.

Permissions apply per user in the `users` list. Keys: `publish`, `subscribe` (each a subject, list or an allow/deny map; a subscribe entry may be `<subject> <queue>` to constrain queue groups, with wildcards), and `allow_responses`. A `permissions` object can use `allow` and `deny` lists explicitly. `default_permissions` applies to users with none of their own.

`allow_responses` (default false) lets a responder publish replies to reply subjects dynamically; true equals `{ max: 1 }` with no time limit; the map form has `max` and `expires` (such as `1s`, `1m`). Enabling it implicitly denies other publishes unless a `publish` allow exists for them, and the reply subject is not checked against the publish lists. With nsc use `--allow-pub-response` and `--response-ttl`.

Example shape (variables):
```
authorization {
  default_permissions = { publish = "SANDBOX.*"  subscribe = ["PUBLIC.>", "_INBOX.>"] }
  REQUESTOR = { publish = ["req.a", "req.b"]  subscribe = "_INBOX.>" }
  RESPONDER = { subscribe = ["req.a", "req.b"]  publish = "_INBOX.>" }
  users = [ {user: client, password: $CLIENT_PASS, permissions: $REQUESTOR}, {user: service, password: $SERVICE_PASS, permissions: $RESPONDER} ]
}
```

Gotchas: do not break request-reply: requesters need subscribe on `_INBOX.>` (or a narrower prefix) and responders publish to it. Anyone allowed `_INBOX.>` can see all responses, so sensitive setups should narrow the prefix or use accounts. A violation is rejected by the server for that operation.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
