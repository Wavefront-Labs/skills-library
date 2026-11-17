---
id: computing-software.messaging-and-integration.rabbitmq.topic-permissions
name: topic-permissions
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, topic-permissions]
level: advanced
status: docs-checked
description: "Restrict routing keys on topic exchanges per user with topic permissions."
sources:
  - https://www.rabbitmq.com/docs/man/rabbitmqctl.8
  - https://www.rabbitmq.com/docs/access-control
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Topic authorization

**Goal:** Limit which routing keys a user may publish or consume on a topic exchange.

## Steps
1. `rabbitmqctl set_topic_permissions -p app1 svc amq.topic "^svc\." "^svc\."` (vhost, user, exchange, write regex on the published routing key, read regex on the consumed routing key).
2. The check applies to the named topic exchange.
3. Variables `username`, `vhost` and `client_id` can be expanded in the patterns (`client_id` only for MQTT), e.g. `"^{username}-.*"`.
4. View entries with `rabbitmqctl list_topic_permissions`.

## Failure modes
- Patterns are regular expressions matched against the routing key; test them before relying on them.

## Verify
- `rabbitmqctl list_topic_permissions -p app1`.

## Checked

2026-11-02. Confirmed in the rabbitmqctl man page: set_topic_permissions arguments, example with amq.topic, variable expansion (username, vhost, client_id), list_topic_permissions. Removed: claims that no entry allows all keys and that a denial is observable on publish (not stated in the pages I read).
Method: documentation only; no commands were run.
