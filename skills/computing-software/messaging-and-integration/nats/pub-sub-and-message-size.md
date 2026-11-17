---
id: computing-software.messaging-and-integration.nats.pub-sub-and-message-size
name: pub-sub-and-message-size
category: computing-software
field: messaging-and-integration
product: nats
tags: [pub-sub, fan-out, max-payload, messages]
level: practitioner
status: docs-checked
description: "NATS core pub-sub fan-out: message anatomy (subject, payload, headers, reply) and the max_payload size limit and its default."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/nats-concepts/core-nats/publish-subscribe/pubsub.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the core one-to-many delivery model and the message size ceiling.

Core NATS publish-subscribe sends a message on a subject to every active subscriber listening on it (fan-out). Subscribers can register interest with wildcard subjects, which behave a little like a regular expression but only a little.

A message is composed of:
1. a subject,
2. a payload that is a byte array,
3. any number of header fields,
4. an optional reply address field.

The maximum message size is the server setting `max_payload`. The default is 1 MB, it can be raised up to 64 MB, but the docs recommend keeping messages more reasonable, around 8 MB at most. Larger blobs belong in the JetStream Object Store, which chunks files, rather than in one core message.

Gotchas: core NATS gives at-most-once delivery to whoever is subscribed at publish time; subscribers that are not connected miss the message, so use a JetStream stream if you need persistence or replay.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
