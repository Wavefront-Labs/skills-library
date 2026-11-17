---
id: computing-software.messaging-and-integration.apache-activemq-artemis.group-first-key
name: group-first-key
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,group-first-key,default-group-first-key,jmsxgroupfirstforconsumer,message-group-ownership,activemq-artemis]
level: advanced
status: docs-checked
description: "Flag the first message a consumer gets for a message group by setting group-first-key on the queue or default-group-first-key in an address-setting."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-grouping.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notifying a consumer of group ownership

**Goal:** let a consumer know that a group has just been assigned to it, so it can initialise state.

Set `group-first-key` at the queue level to a header name of your choice (the manual uses `JMSXGroupFirstForConsumer`). Each time a new group is assigned to a consumer, the broker sets that header to `true` on the first message sent to the consumer for that group.
```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" group-first-key="JMSXGroupFirstForConsumer"/>
   </multicast>
</address>
```
For auto-created destinations from the Core JMS client use an address parameter: `session.createQueue("my.destination.name?group-first-key=JMSXGroupFirstForConsumer")`.

To default every queue under an address:
```xml
<address-setting match="my.address">
   <default-group-first-key>JMSXGroupFirstForConsumer</default-group-first-key>
</address-setting>
```
The feature is off by default.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-grouping, section Notifying Consumer of Group Ownership change: queue attribute, header key, JMS address parameter, default-group-first-key, off by default. Removed: the Verify step and a notes section with unsupported restart claims.
Method: documentation only; no commands were run.
