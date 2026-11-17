---
id: computing-software.messaging-and-integration.apache-camel.idempotent-consumer
name: idempotent-consumer
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, idempotent-consumer, duplicates, repository]
level: practitioner
status: docs-checked
description: "Camel Idempotent Consumer EIP: eager, skipDuplicate and removeOnFailure defaults, CamelDuplicateMessage and available repositories."
sources:
  - https://camel.apache.org/components/next/eips/idempotentConsumer-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Idempotent Consumer

Filters duplicates. Camel adds the id eagerly to the repository; on completion it removes the id if the exchange failed, otherwise it stays.

Options (defaults):
- `expression` required: the unique id
- `idempotentRepository` required
- `eager` true
- `completionEager` false
- `skipDuplicate` true
- `removeOnFailure` true
- `disabled` false

Property: `CamelDuplicateMessage` is `true` for duplicates. With `skipDuplicate(false)` duplicates pass through with that property set, so a `choice` can branch on `${exchangeProperty.CamelDuplicateMessage} == true`.

Repositories:
- In camel-support: `MemoryIdempotentRepository` (keeps the last 1,000 ids; lost on stop) and `FileIdempotentRepository` (persists).
- Component-based: Caffeine, Cassandra, EHCache, Hazelcast, Infinispan, JCache, JPA (`JpaMessageIdRepository`), Kafka (`KafkaIdempotentRepository`), MongoDB, Redis, Spring Cache, JDBC (`JdbcMessageIdRepository`).
- Custom: implement `org.apache.camel.spi.IdempotentRepository`.

```java
.idempotentConsumer(header("messageId"), MemoryIdempotentRepository.memoryIdempotentRepository())
```

In XML and YAML declare the repository as a bean and reference it.

Verify: two messages with the same `messageId` reach `mock:result` once.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Idempotent Consumer EIP page source (idempotentConsumer-eip.adoc) and the model definition (idempotentConsumer.json) from the apache/camel repository, which generate the cited page. Confirmed eager add and removal on failure, the option defaults (eager true, completionEager false, skipDuplicate true, removeOnFailure true, disabled false), required expression and idempotentRepository, CamelDuplicateMessage, the repository list, MemoryIdempotentRepository keeping 1000 ids in memory, and the XML and YAML bean note. Removed the unsupported remark that the property is available after the EIP. No commands were run.
