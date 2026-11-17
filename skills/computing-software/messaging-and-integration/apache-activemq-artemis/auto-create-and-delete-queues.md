---
id: computing-software.messaging-and-integration.apache-activemq-artemis.auto-create-and-delete-queues
name: auto-create-and-delete-queues
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,auto-create-queues,auto-delete-queues,auto-delete-queues-delay,address-queue-scan-period,auto-delete-created-queues,activemq-artemis]
level: practitioner
status: docs-checked
description: "Control automatic queue creation and deletion with auto-create-queues, auto-delete-queues, its delay and message-count limits and the usage check."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/address-settings.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-created queues: create and delete

**Goal:** decide whether queues appear on demand and when they disappear.

## Create
`auto-create-queues` (default `true`): create a queue when a message is sent or a consumer connects to a queue whose address fits the `match`. Auto-created queues are durable, non-temporary and non-transient. It does not work for the Core client, because the Core API is low-level and not meant for such automation.

## Delete
- `auto-delete-queues` (default true): delete auto-created queues that have 0 consumers and a message count at or below `auto-delete-queues-message-count` (default `0`, i.e. empty; `-1` disables the count check).
- `auto-delete-created-queues` (default `false`): same rule applied to queues that were created (not auto-created).
- `auto-delete-queues-delay` (ms, default `0` = immediately): wait after the queue meets the conditions.
- `address-queue-scan-period` (broker setting, ms, default `30000`, `-1` disables scanning): how often queues and addresses are scanned for deletion.
- `auto-delete-queues-skip-usage-check` (default `false`): by default a queue is deleted only if it was "used" (a message was sent or a consumer connected). When `true` you must also set `auto-delete-queues-delay` above 0, or queues may vanish almost immediately; deletion is then based on creation time.

Clients can override per queue: Core API `createQueue` parameters, or JMS destination attributes such as `my.destination?auto-delete=true&auto-delete-delay=120000&auto-delete-message-count=-1`.

## Verify
Connect and disconnect a consumer on a fresh name and confirm the queue is removed after the delay plus up to one scan period.

## Checked

Method: docs-checked 2026-11-09 against address-settings.adoc (raw, auto-create/delete queue entries)
