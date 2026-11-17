---
id: computing-software.messaging-and-integration.redpanda.acl-recipes-for-producers-consumers-and-transactions
name: acl-recipes-for-producers-consumers-and-transactions
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [acl, producer, consumer, transactional-id, consumer-group, kafka-requests, permissions]
level: practitioner
status: docs-checked
description: "Which ACLs each client needs: simple producer, consumer with group, transactional producer and group admin, plus the per-request operation requirements such as InitProducerID."
sources:
  - https://docs.redpanda.com/streaming/current/manage/security/authorization/acl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Quick reference**

| Client | Required ACLs |
|---|---|
| Simple producer | WRITE + DESCRIBE on target topics |
| Simple consumer | READ + DESCRIBE on topics, READ on the consumer group |
| Transactional producer | WRITE + DESCRIBE on topics, WRITE on the transactional ID |
| Consumer group admin | READ + DESCRIBE on topics, READ + DESCRIBE + DELETE on groups |

```bash
rpk security acl create --allow-principal producer-user \
  --operation write,describe --topic my-topic
rpk security acl create --allow-principal consumer-user \
  --operation read,describe --topic my-topic
rpk security acl create --allow-principal consumer-user \
  --operation read --group my-consumer-group
```

**Per Kafka request** (from the page's list):
- Produce: WRITE on the topic, plus WRITE on TRANSACTIONAL_ID for a `transaction.id`.
- Fetch: READ on the topic. ListOffsets and OffsetForLeaderEpoch: DESCRIBE on the topic.
- Metadata: DESCRIBE on the topic; auto-creating topics also needs CREATE on the cluster or topic.
- InitProducerID: IDEMPOTENT_WRITE on the cluster, or WRITE on any topic, or WRITE on the transactional ID when using transactions.
- FindCoordinator: DESCRIBE on the group (and on the transactional ID for transactions).
- OffsetCommit: READ on the group and topic. OffsetFetch: DESCRIBE on the group and topic.
- OffsetDelete: DELETE on the group and READ on the topic.

Admin pattern: `ALL` on the cluster and specific resources. The Console's "Allow all operations" button is for testing only.

## Checked

The quick reference table, commands and the request-to-operation list were confirmed on the Configure Access Control Lists page. An unconfirmed troubleshooting sentence was removed.

Method: docs-checked 2026-11-09 against the Configure Access Control Lists page (quick reference, request operations table, rpk flags), read in part; no commands were run.
