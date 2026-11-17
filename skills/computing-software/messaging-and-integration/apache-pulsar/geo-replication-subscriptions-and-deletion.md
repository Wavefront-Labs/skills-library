---
id: computing-software.messaging-and-integration.apache-pulsar.geo-replication-subscriptions-and-deletion
name: geo-replication-subscriptions-and-deletion
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [geo-replication, local-subscriptions, replicated-subscriptions, topic-deletion, cascading-deletion, inactive-topics]
level: advanced
status: docs-checked
description: "Understand what Pulsar geo-replication does not replicate (subscriptions) and delete geo-replicated topics safely without orphaning or cascading surprises."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/concepts-replication.md
  - https://github.com/apache/pulsar-site/blob/main/docs/administration-geo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid wrong assumptions about consumers across clusters and delete replicated topics without surprises.

What replicates: topic data. Subscriptions, cursors, consumers, backlog and acknowledgment state do not. Only the mark-delete position of a replicated subscription can be synchronized, if explicitly enabled; individual acks are never replicated. Replicated subscriptions require two-way geo-replication.

Consequences:
- The same subscription name in two clusters creates two independent subscriptions, each with its own cursor and subscription type.
- A consumer reconnecting to another cluster does not resume the original subscription; it starts a new unrelated one.
- Consumers sharing a name across clusters do not form one consumer group and do not split work; to share load across regions, shard at topic or partition level.
- Deleting a replicated topic requires deleting local subscriptions in every cluster.

Recommended explicit deletion:
1. Ensure no active producers or consumers exist in any cluster (otherwise the topic is forcibly deleted from under them, and auto-creation may recreate it).
2. Set a global topic-level `clusters` policy that includes only the local cluster; this triggers cascading deletion on excluded clusters, including partitions, schemas and local policies.
3. Delete the topic (now only local).
4. Run `pulsar-admin topicPolicies delete <topic>` on each cluster.
Skipping this leaves the topic orphaned on peers with replication still active.

Garbage collection also deletes an inactive replicated topic when `brokerDeleteInactiveTopicsEnabled=true` and nothing is connected, subject to `brokerDeleteInactiveTopicsMode` (`delete_when_no_subscriptions` or `delete_when_subscriptions_caught_up`).

Gotcha: changing the namespace or topic `clusters` setting can itself delete topics on excluded clusters. Keep independent backups if accidental deletion is unacceptable.

Verify: after step 4, list the topic in every cluster and confirm it is gone.

## Checked

Method: docs-checked 2026-11-09 against pulsar-site docs/concepts-replication.md (read in full) and docs/administration-geo.md (deletion, cascading deletion and replicated subscription sections read)
