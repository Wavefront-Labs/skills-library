---
id: computing-software.messaging-and-integration.rabbitmq.users-and-vhosts
name: users-and-vhosts
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, users-and-vhosts, rmq-access-control]
level: intro
status: docs-checked
description: "Create users, virtual hosts and permissions with rabbitmqctl and remove the default guest account."
sources:
  - https://www.rabbitmq.com/docs/access-control
  - https://www.rabbitmq.com/docs/vhosts
  - https://www.rabbitmq.com/docs/man/rabbitmqctl.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Users and virtual hosts

**Goal:** Isolate tenants and enforce least privilege.

## Steps
1. `rabbitmqctl add_vhost app1`; `rabbitmqctl add_user svc` (prompts for the password, or pipe it on stdin as the access-control guide shows).
2. `rabbitmqctl set_permissions -p app1 svc "^svc\." "^svc\." "^svc\."` (configure, write, read regexes).
3. Production environments should not use the default `guest` user: create new accounts, then remove or restrict it with `rabbitmqctl delete_user guest`.
4. `rabbitmqctl set_user_tags svc monitoring` for management UI roles (tags: management, policymaker, monitoring, administrator).

## Failure modes
- The pattern `^$` (or the empty string `''`) matches nothing and stops the user performing any operation on that permission; `.*` matches every resource.
- A password given as a command-line argument ends up in shell history; prompt for it or pipe it on stdin.
- Permission checks can be cached per connection or channel, so permission changes may need a reconnect to take effect.

## Verify
- `rabbitmqctl list_permissions -p app1` and `rabbitmqctl list_users`.

## Checked

2026-11-02. Confirmed in docs/access-control: add_user (prompt and stdin forms), set_permissions, delete_user, list_users, list_permissions, the `^$`/empty-string rule, guest warning, permission-check caching; docs/vhosts: add_vhost; management guide: user tag names. Removed: the literal-password example and env-var advice (not in the pages).
Method: documentation only; no commands were run.
