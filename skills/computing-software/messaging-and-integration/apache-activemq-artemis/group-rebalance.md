---
id: computing-software.messaging-and-integration.apache-activemq-artemis.group-rebalance
name: group-rebalance
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,group-rebalance,group-rebalance-pause-dispatch,resetallgroups,default-group-rebalance,activemq-artemis]
level: advanced
status: docs-checked
description: "Rebalance message groups onto new consumers with the resetAllGroups operation or group-rebalance, and pause dispatch with group-rebalance-pause-dispatch."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-grouping.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rebalancing message groups

**Problem:** new consumers get no groups, because all groups are already pinned to existing consumers, so the new consumers sit idle.

## Manual
Invoke `resetAllGroups` on the queue through the management API (for example the web console).

## Automatic
Set `group-rebalance` to `true` on the queue so each added consumer triggers a reset/rebalance. By default the broker keeps dispatching during rebalance. To make sure in-flight messages are processed before new messages are dispatched to different consumers, also set `group-rebalance-pause-dispatch` to `true`, which pauses dispatch during rebalance until in-flight messages finish.
```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" group-rebalance="true" group-rebalance-pause-dispatch="true"/>
   </multicast>
</address>
```
JMS address parameters: `my.destination.name?group-rebalance=true&group-rebalance-pause-dispatch=true`. Address-wide defaults: `default-group-rebalance` and `default-group-rebalance-pause-dispatch` in an address-setting, both `false` by default.

## Risk
At the instant of a reset, a message to the original consumer may still be in flight while a new message of the same group goes to the new consumer, and the manual advises pausing dispatch to let in-flight messages finish.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-grouping, section Rebalancing Message Groups: resetAllGroups, group-rebalance, group-rebalance-pause-dispatch, address-setting defaults. Removed: the Verify step and an ordering claim not on the page.
Method: documentation only; no commands were run.
