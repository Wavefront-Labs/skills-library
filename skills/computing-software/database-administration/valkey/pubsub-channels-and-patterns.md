---
id: computing-software.database-administration.valkey.pubsub-channels-and-patterns
name: pubsub-channels-and-patterns
category: computing-software
field: database-administration
product: valkey
tags: [pubsub, subscribe, psubscribe, publish, ssubscribe, spublish, sharded-pubsub, at-most-once]
level: practitioner
status: docs-checked
description: "Valkey Pub/Sub: SUBSCRIBE, PSUBSCRIBE, PUBLISH, at-most-once delivery, message formats, db scoping, RESP2 restrictions and sharded SSUBSCRIBE/SPUBLISH."
sources:
  - https://valkey.io/topics/pubsub/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Publishers `PUBLISH` to channels without knowing receivers; subscribers `SUBSCRIBE` to channels and receive only matching messages in publish order. Channels are not persisted: with no subscriber the message is lost, and delivery is at-most-once (a subscriber that errors or disconnects loses it forever). For durability or at-least-once, use Streams.

A RESP2 client in subscribed state should not issue other commands; allowed are `PING`, `PSUBSCRIBE`, `PUNSUBSCRIBE`, `QUIT`, `RESET`, `SSUBSCRIBE`, `SUBSCRIBE`, `SUNSUBSCRIBE`, `UNSUBSCRIBE`. Under RESP3 (`HELLO`) any command is allowed. `valkey-cli` in subscribed mode only exits with Ctrl-C.

Pushed messages are 3-element arrays: `subscribe`/`unsubscribe` (channel, then the count of remaining subscriptions; zero means you left Pub/Sub state) and `message` (channel, payload). Patterns: `PSUBSCRIBE news.*` accepts any glob pattern; `PUNSUBSCRIBE news.*` removes it. Matches arrive as `pmessage` (pattern, channel, payload). A client subscribed to both `foo` and `f*` receives two messages for a publish to `foo`. The count includes channels plus patterns.

Scoping: Pub/Sub ignores database numbers, so publishing on db 10 reaches a subscriber on db 1; prefix channels with the environment name (test, staging, production).

Sharded Pub/Sub (`SSUBSCRIBE`, `SUNSUBSCRIBE`, `SPUBLISH`): shard channels hash to slots like keys; publish goes to a node owning the slot, is forwarded only within that shard, and subscribers may connect to the primary or its replicas. This limits cluster-bus traffic versus global Pub/Sub, so adding shards scales it.

Client hint: map each original subscription (channel or pattern) to a callback in a hash table for O(1) dispatch.

## Checked

2026-11-03. Confirmed against https://valkey.io/topics/pubsub/ (page text read in full): Channels not persisted, at-most-once delivery, Streams alternative, allowed RESP2 commands, RESP3 exception, valkey-cli Ctrl-C, message formats, database scoping, PSUBSCRIBE/pmessage, double delivery for foo and f*, subscription count, sharded Pub/Sub, hash-table callback hint.

Removed or changed: Nothing removed; no claim in the skill went beyond the page.

Method: documentation only; no commands were run.
