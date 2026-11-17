---
id: computing-software.messaging-and-integration.apache-pulsar.backlog-quotas
name: backlog-quotas
category: computing-software
field: messaging-and-integration
product: apache-pulsar
tags: [backlog-quota, producer-request-hold, producer-exception, consumer-backlog-eviction, set-backlog-quota]
level: practitioner
status: docs-checked
description: "Cap Pulsar topic backlogs with namespace backlog quotas: size or time limits, the three eviction policies, set/get/remove commands and clear-backlog."
sources:
  - https://github.com/apache/pulsar-site/blob/main/docs/cookbooks-retention-expiry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stop unacknowledged backlogs from growing without bound.

A backlog is the set of unacknowledged messages stored for a topic. A backlog quota sets a hard limit on its logical size and/or age for each topic in a namespace, plus a policy for what the broker does when the limit is exceeded:
- `producer_request_hold`: the producer holds the message and retries until the client `sendTimeoutMs` is exceeded.
- `producer_exception`: the producer throws an exception when sending.
- `consumer_backlog_eviction`: the broker starts discarding backlog messages.

Commands:
```shell
pulsar-admin namespaces set-backlog-quota my-tenant/my-ns --limit 2G --policy producer_request_hold
pulsar-admin namespaces set-backlog-quota my-tenant/my-ns/my-topic --limitTime 3600 --policy producer_request_hold --type message_age
pulsar-admin namespaces get-backlog-quotas my-tenant/my-ns
pulsar-admin namespaces remove-backlog-quota my-tenant/my-ns
pulsar-admin namespaces clear-backlog my-tenant/my-ns
```
Flags: `-l/--limit` size, `-lt/--limitTime` seconds, `-p/--policy`, `-t/--type` (default `destination_storage`). `clear-backlog` prompts for confirmation unless `-f/--force`. Java: `admin.namespaces().setBacklogQuota(namespace, BacklogQuota.builder().retentionPolicy(RetentionPolicy.producer_request_hold).limitSize(...).limitTime(...).build())`.

Gotcha: retention scope includes the backlog, so the retention setting must be greater than the backlog quota or Pulsar returns an error when both are set.

Monitoring: quota limit and usage are exposed in topic metrics and topic stats, so alert before the limit is reached.

## Checked

2026-11-03. Confirmed against the pulsar-site page cookbooks-retention-expiry (Backlog quotas section): the three policies, flags, set/get/remove/clear-backlog commands, Java builder, retention-versus-quota note and monitoring statement. Removed the invented Verify step.

Method: documentation only; no commands were run.
