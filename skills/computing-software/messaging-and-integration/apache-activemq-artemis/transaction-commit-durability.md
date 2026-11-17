---
id: computing-software.messaging-and-integration.apache-activemq-artemis.transaction-commit-durability
name: transaction-commit-durability
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,journal-sync-transactional,journal-sync-non-transactional,commit,durability,send-guarantees,activemq-artemis]
level: advanced
status: docs-checked
description: "Control whether commits and rollbacks are fsynced before the reply using journal-sync-transactional (default true), trading durability for speed."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/send-guarantees.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Transaction commit durability

When a client commits or rolls back, the call blocks until the server replies. The server writes the commit to the journal, and `journal-sync-transactional` in `broker.xml` decides whether it ensures durable persistence before replying.

- `true` (default): by the time `commit` or `rollback` returns, it is persisted to storage.
- `false`: the reply may be sent before persistence; a server failure may lose the commit or rollback. This improves performance at the cost of some transaction durability.

For non-transactional sends, a durable message routed to at least one durable queue is persisted by the server. With `journal-sync-non-transactional` (default `true`) the server does not reply until persistence is guaranteed on disk.

```xml
<journal-sync-transactional>true</journal-sync-transactional>
<journal-sync-non-transactional>true</journal-sync-non-transactional>
```

Lowering either value is only appropriate when losing the last few operations on a crash is acceptable.

## Checked

Method: docs-checked 2026-11-09 against send-guarantees.adoc (read in full). Removed the Verify step and unsupported advice.
