---
id: computing-software.messaging-and-integration.apache-activemq-artemis.message-grouping
name: message-grouping
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,message-grouping,jmsxgroupid,amq-group-id,autogroup,jmsxgroupseq,group-id,activemq-artemis]
level: practitioner
status: docs-checked
description: "Pin all messages with the same group id to one consumer using JMSXGroupID or _AMQ_GROUP_ID, autoGroup, a factory-level groupID, or close a group with JMSXGroupSeq -1."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-grouping.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Message grouping

**Goal:** process all messages for a key (for example one stock) serially on the same consumer even with many consumers on the queue. If that consumer closes, another is chosen and receives the group.

## Set the group
- Core API: property `_AMQ_GROUP_ID` (constant `MessageImpl.HDR_GROUP_ID`), or `autogroup=true` on the `SessionFactory` for a random unique id.
- JMS: `message.setStringProperty("JMSXGroupID", "Group-0");` or `autoGroup=true` on the connection factory.
- Per connection factory, JNDI `jndi.properties`:
```properties
java.naming.factory.initial=org.apache.activemq.artemis.jndi.ActiveMQInitialContextFactory
connectionFactory.myConnectionFactory=tcp://localhost:61616?groupID=Group-0
```
`?autoGroup=true` works the same way; `groupID` stamps every message from producers created by that factory.

## Closing a group
You normally never need to. To close one, send a message with the group id plus `message.setIntProperty("JMSXGroupSeq", -1);`. A later message with the same id is assigned to a new consumer.

## Head-of-line caution
Grouped messages interact with queue FIFO order: 100 grouped messages at the head followed by 1,000 ungrouped ones must all go to their consumer before the ungrouped can be consumed, temporarily suspending concurrent processing. Size groups accordingly or isolate grouped from ungrouped traffic. Combining groups with clustering is discouraged (see `clustered-message-grouping`).

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-grouping: group properties, autogroup, groupID URL parameter, JMSXGroupSeq -1 close, FIFO note. Removed: the Verify step.
Method: documentation only; no commands were run.
