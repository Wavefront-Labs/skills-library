---
id: computing-software.messaging-and-integration.rabbitmq.quorum-queue-migration
name: quorum-queue-migration
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, quorum-queue-migration]
level: advanced
status: docs-checked
description: "Migrate classic queues to quorum queues by declaring new queues, shoveling messages and switching clients, since queue type cannot change in place."
sources:
  - https://www.rabbitmq.com/docs/quorum-queues
  - https://www.rabbitmq.com/kubernetes/operator/using-topology-operator
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quorum queue migration

**Goal:** Move traffic with no data loss.

## Steps
1. Declare the new quorum queue under a new name (or vhost) with the `x-queue-type` argument set to `quorum`, and bind it to the same exchanges. The type must be given at declaration; it cannot be set or changed via a policy.
2. Drain the old queue with a shovel or consumers into the new one.
3. Switch publishers and consumers, then delete the old queue when empty.
4. For a blue-green cutover from 3.13.x mirrored classic queues, see the "Migrating from RabbitMQ 3.13.x ... Using Blue-Green Deployment" section of the quorum queues guide.

## Verify
- `rabbitmqctl list_queues name type messages`: old at 0, new carrying traffic.

## Checked

2026-11-02. Confirmed in docs/quorum-queues: x-queue-type quorum at declaration only, blue-green migration section; using-topology-operator: a Shovel example named migrate-to-quorum; rabbitmqctl man page: list_queues type and messages items. Removed: the PRECONDITION_FAILED claim for changing x-queue-type (not stated in pages).
Method: documentation only; no commands were run.
