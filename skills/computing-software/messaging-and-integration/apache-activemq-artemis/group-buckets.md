---
id: computing-software.messaging-and-integration.apache-activemq-artemis.group-buckets
name: group-buckets
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,group-buckets,default-group-buckets,message-groups-memory,hashing,activemq-artemis]
level: advanced
status: docs-checked
description: "Bound memory used by message groups by hashing group ids into group-buckets (default -1 tracks every group; 0 disables grouping on a queue)."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/message-grouping.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group buckets

**Goal:** scale message groups with bounded memory. By default the queue tracks every distinct group id, which can use unbounded memory; with buckets the group id is hashed into one of N buckets.

- `group-buckets` = `-1` (default): keep every group (unbounded memory).
- `group-buckets` = `0`: disable grouping on that queue. Useful on a multicast address with many queues where one queue does not need ordering and should round-robin.
- `group-buckets` = N: hash into N buckets, for example `1024`.

```xml
<address name="foo.bar">
   <multicast>
      <queue name="orders1" group-buckets="1024"/>
   </multicast>
</address>
```
Other ways: pass `group-buckets` to the Core API queue creation, JMS address parameter `my.destination.name?group-buckets=1024`, or address-wide `default-group-buckets` (default `-1`) in an address-setting, with wildcards for sets of addresses.

## Checked
2026-11-03. Confirmed against the Artemis user manual page message-grouping, section Group Buckets: values -1 and 0, XML, address parameter, default-group-buckets and default. Removed: the Verify step and a distribution trade-off claim the page does not make.
Method: documentation only; no commands were run.
