---
id: computing-software.messaging-and-integration.rabbitmq.topic-exchange-wildcards
name: topic-exchange-wildcards
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, topic-exchange-wildcards, rmq-bindings]
level: practitioner
status: docs-checked
description: "Write topic bindings with dot-separated words, star for exactly one word and hash for zero or more."
sources:
  - https://www.rabbitmq.com/docs/exchanges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topic exchange wildcards

**Goal:** Route by hierarchical keys such as `region.service.severity`.

## Steps
1. A routing key is a list of dot-separated words.
2. `*` matches exactly one word; `#` matches zero or more words.
3. Bind the queue to the topic exchange with binding key `*.error`.
4. A binding key of `#` alone matches any routing key and makes the topic exchange act like a fanout for that binding.

## Failure modes
- Using `*` expecting multi-word matches leads to missed messages.

## Verify
- Publish `eu.error` and `eu.info.extra`; only the first reaches the `*.error` queue.

## Checked

Date: 2026-11-02. Confirmed in the Exchanges guide (docs/exchanges): `*` is exactly one segment, `#` zero or more, `#` acts like fanout. Removed as not stated there: the 255-byte key limit, the `rabbitmqadmin declare binding` command, the direct-like remark and the binding-count performance note.

Method: documentation only; no commands were run.
