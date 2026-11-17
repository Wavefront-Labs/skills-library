---
id: computing-software.messaging-and-integration.rabbitmq.message-and-resource-limits
name: message-and-resource-limits
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, message-and-resource-limits]
level: advanced
status: docs-checked
description: "Apply per-vhost and per-user limits on connections, channels and queues to stop noisy tenants."
sources:
  - https://www.rabbitmq.com/docs/vhosts
  - https://www.rabbitmq.com/docs/user-limits
  - https://www.rabbitmq.com/docs/limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource limits for tenants

**Goal:** Protect against exhaustion.

## Steps
1. Per virtual host, one limit per command: `rabbitmqctl set_vhost_limits -p app1 '{"max-connections": 100}'` and `rabbitmqctl set_vhost_limits -p app1 '{"max-queues": 500}'`. A `max-connections` of zero blocks client connections to the vhost.
2. Per user: `rabbitmqctl set_user_limits svc '{"max-connections": 50}'`. The user `max-channels` limit counts channels across all of the user's connections, so keep it at or above the connection limit.
3. Cap message size with `max_message_size` in `rabbitmq.conf` (default 16777216 bytes, maximum 512 MiB); larger messages are rejected.

## Failure modes
- A limit set too low will reject new connections or queue declarations at the limit.

## Verify
- `rabbitmqctl list_vhost_limits` and `rabbitmqctl list_user_limits svc`.

## Checked

Date: 2026-11-02. Confirmed on the Virtual Hosts, User Limits and Configurable Limits pages: commands, limit names, zero blocks connections, `max_message_size` default and maximum. Changed: the combined two-key vhost JSON is not shown in the guide, so it is split into two commands. Removed: "spikes" wording.

Method: documentation only; no commands were run.
