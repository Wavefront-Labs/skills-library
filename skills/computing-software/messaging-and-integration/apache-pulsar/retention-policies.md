---
id: computing-software.messaging-and-integration.apache-pulsar.retention-policies
name: retention-policies
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [retention, set-retention, retention-size, retention-time, default-retention-time-in-minutes, reader]
level: practitioner
status: docs-checked
description: "Keep acknowledged Pulsar messages with namespace retention: size and time limit semantics (-1 and 0), set-retention commands, defaults and Reader use."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-retention-expiry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: retain already-acknowledged (or never-subscribed) messages for a bounded time or size.

By default a broker keeps only messages that are in at least one subscription backlog, so a topic without subscriptions retains nothing. Deleted messages may stay readable until the next ledger rollover; do not rely on that. Retention is useful for the Reader interface, which does not acknowledge, so Reader-only use cases must configure retention.

Both a size limit and a time limit must be set. Meaning of the pair (time, size):
- (-1, -1) infinite; (-1, >0) size only; (>0, -1) time only.
- (0, 0) disabled, which is the default.
- (0, >0) or (>0, 0) invalid.
- (>0, >0) messages are dropped when either limit is reached.

Instance defaults are `defaultRetentionTimeInMinutes` and `defaultRetentionSizeInMB`, both `0` (disabled). Retention applies to topics with no subscriptions and to messages acked by all subscriptions; it does not affect unacknowledged messages on topics that have subscriptions. When a limit is exceeded the oldest message is marked for deletion until limits hold.

Commands (namespace level):
```shell
pulsar-admin namespaces set-retention my-tenant/my-ns --size 10G --time 3h
pulsar-admin namespaces set-retention my-tenant/my-ns --size -1 --time -1   # infinite
pulsar-admin namespaces set-retention my-tenant/my-ns --size 0 --time 0     # disable
pulsar-admin namespaces get-retention my-tenant/my-ns
```
The get output is JSON with `retentionTimeInMinutes` and `retentionSizeInMB`. Java equivalent: `admin.namespaces().setRetention(namespace, new RetentionPolicies(retentionTime, retentionSize))`, time in minutes and size in MB.

Gotcha: retention keeps data for at least the window; TTL discards unacknowledged data. Most applications want at most one of them.

## Checked

2026-11-03. Confirmed against the pulsar-site page cookbooks-retention-expiry (Retention policies section): the time/size table, instance defaults, set/get-retention commands, JSON keys and Java call. Removed the invented Verify step.

Method: documentation only; no commands were run.
