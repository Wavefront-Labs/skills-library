---
id: computing-software.messaging-and-integration.nats.subject-naming-and-wildcards
name: subject-naming-and-wildcards
category: computing-software
field: messaging-and-integration
product: nats
tags: [subjects, subject-hierarchy, wildcards, naming]
level: practitioner
status: docs-checked
description: "Design NATS subject hierarchies: token limits, naming guidelines, wildcard use, and memory cost of many subscriptions."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/subjects.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose subject names that stay cheap for the server and easy to secure, filter and map.

- A subject is a dot-separated string. The `.` creates a hierarchy such as `time.us.east.atlanta`; wildcards let one subscription cover several levels.
- Docs recommend at most about 16 tokens and under 256 characters per subject, though there is no hard limit.
- NATS handles tens of millions of subjects, but subscription interest is cached in server memory: past one million subscribed subjects expect more than 1GB, growing linearly.
- Subjects are ephemeral and vanish once nobody is subscribed. A subject should carry more than one message and a subscription should be stable (receive more than one message).
- Put a general namespace in the first token(s) (`factory1.tools.group42.unit17`) and identifiers in the last token(s) (`service.deploy.server-acme.app123`). Encode business intent and entity names, not technical details or bulk data.
- Prefer one wildcard subscription over many individual subscriptions.
- A well-designed hierarchy makes per-user allow/deny, account import/export, subject transforms, JetStream stream bindings, source/mirror filters and leaf-node connections much simpler, because all of these filter on subject.

Gotchas: do not over-complicate the design at the start; messages published to a subject with no subscribers are discarded unless a JetStream stream captures them. "Stream" in NATS means JetStream storage, not a topic.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
