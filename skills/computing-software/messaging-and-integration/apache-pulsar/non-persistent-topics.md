---
id: computing-software.messaging-and-integration.apache-pulsar.non-persistent-topics
name: non-persistent-topics
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [non-persistent-topics, in-memory, enable-non-persistent-topics, best-effort, topic-name]
level: practitioner
status: docs-checked
description: "Use Pulsar non-persistent topics for fast, best-effort delivery: naming, loss behaviour on disconnect or broker failure, and the broker switch to disable them."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-messaging.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: trade durability for lower latency on data where loss is acceptable.

Naming: persistent topics use `persistent://tenant/namespace/topic`; non-persistent ones use `non-persistent://tenant/namespace/topic`. The `non-persistent` prefix is the only client-side difference; producers and consumers connect the same way, and exclusive, shared, key_shared and failover subscriptions are all supported. Example consumer topic: `non-persistent://public/default/my-topic` with `client.newConsumer().topic(npTopic).subscriptionName(...).subscribe()`.

Behaviour: the broker does not write messages to BookKeeper. It forwards them straight to connected consumers and acks the producer as soon as delivery is done. There is no buffer even in memory beyond the transfer, so a message in flight when a subscriber disconnects, or when the broker fails, is lost and never redelivered. This makes non-persistent delivery usually faster than persistent.

Broker control: non-persistent topics are enabled by default; disable them with the broker option `enableNonPersistentTopics`. Manage them with the `pulsar-admin topics` command.

Gotchas stated in the docs:
- Non-partitioned non-persistent topics are not stored in ZooKeeper, so if the owning broker crashes they are not reassigned to another broker; they exist only in the owner's memory. The documented workaround is to set `allowAutoTopicCreation` to true so the topic is recreated on demand.
- If a subscriber is disconnected, in-transit messages cannot be delivered later.

Verify: publish to a non-persistent topic with no consumer attached and confirm a consumer attaching afterwards receives nothing.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/concepts-messaging.md (Topics and Non-persistent topics sections read)
