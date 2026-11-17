---
id: computing-software.messaging-and-integration.apache-activemq-artemis.persist-delivery-count-before-delivery
name: persist-delivery-count-before-delivery
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,persist-delivery-count-before-delivery,delivery-count,redelivered,jms-semantics,activemq-artemis]
level: advanced
status: docs-checked
description: "Restore strict JMS redelivered semantics after a crash by persisting the delivery count before delivery, at a performance cost."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/undelivered-messages.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Persisting delivery count before delivery

**Problem:** by default the delivery count is not persisted until a message is rolled back. After a broker crash, a message that had been delivered but not acknowledged is redelivered with `redelivered` set to `false`, when it should be `true`. That breaks strict JMS semantics.

**Why it is off:** persisting the count before each delivery adds an extra persistent step per delivered message, a significant performance penalty for the common case where messages are consumed and acknowledged immediately.

## Enable
In `broker.xml`:
```xml
<persist-delivery-count-before-delivery>true</persist-delivery-count-before-delivery>
```
## Checked
2026-11-03. Confirmed against the Artemis user manual page undelivered-messages, section Delivery Count Persistence: default behaviour, crash effect on the redelivered flag, performance reason, setting and value. Removed: the Verify step and a Related section about max-delivery-attempts that the page does not state.
Method: documentation only; no commands were run.
