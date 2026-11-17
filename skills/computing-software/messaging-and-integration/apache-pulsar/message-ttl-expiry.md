---
id: computing-software.messaging-and-integration.apache-pulsar.message-ttl-expiry
name: message-ttl-expiry
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [message-ttl, expiry, set-message-ttl, unacknowledged-messages, cursor]
level: practitioner
status: docs-checked
description: "Expire unacknowledged Pulsar messages with a namespace TTL: set-message-ttl in seconds, auto-ack behaviour, reader cursor caveat and get/remove commands."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-retention-expiry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound disk usage from messages that consumers never acknowledge.

By default Pulsar stores unacknowledged messages forever. A time to live (TTL) is a stopwatch per message: when it expires, Pulsar automatically moves the message to the acknowledged state, making it ready for deletion. Retention and TTL solve different problems (keep acknowledged data at least X hours versus discard data after some time), and most applications use at most one.

Commands (TTL in seconds):
```shell
pulsar-admin namespaces set-message-ttl my-tenant/my-ns --messageTTL 120
pulsar-admin namespaces get-message-ttl my-tenant/my-ns
pulsar-admin namespaces remove-message-ttl my-tenant/my-ns
```
The flag is `-ttl/--messageTTL`. Java: `admin.namespaces().setNamespaceMessageTTL(namespace, ttlInSeconds)`, `getNamespaceMessageTTL(namespace)`, `removeNamespaceMessageTTL(namespace)`.

Caveats stated in the page:
- Expiry advances durable subscription cursors only. It does not advance non-durable Reader cursors past unread retained messages, so a Reader is not a retention mechanism; configure a retention policy for data a Reader needs.
- Changing TTL to a positive value schedules the expiry check in the background. When the policy update call returns, not every newly expired message has necessarily been acknowledged; the periodic expiry monitor also checks them.

## Checked

2026-11-03. Confirmed against the pulsar-site page cookbooks-retention-expiry (Time to live section): default behaviour, set/get/remove-message-ttl commands, `-ttl`/`--messageTTL` flag in seconds, Java methods, both caveats. Removed the unsourced disk-reclaim caveat and the invented Verify step.

Method: documentation only; no commands were run.
