---
id: computing-software.messaging-and-integration.rabbitmq.management-ui
name: management-ui
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, management-ui, rmq-management]
level: intro
status: docs-checked
description: "Use the management UI on port 15672 for overview, queues, exchanges, connections, policies and users, with TLS and restricted access."
sources:
  - https://www.rabbitmq.com/docs/management
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management UI

**Goal:** Operate through the UI safely.

## Steps
1. `rabbitmq-plugins enable rabbitmq_management`; browse to port 15672 (15671 for HTTPS).
2. Give users tags as needed: management, policymaker, monitoring or administrator.
3. Configure TLS for the management listener and restrict access to it with a firewall.

## Failure modes
- Exposing 15672 to the internet is a risk.

## Verify
- Log in as a monitoring user and check what is visible against the tag descriptions in the guide.

## Checked

2026-11-02. Confirmed in docs/management: ports 15672/15671, tag names and descriptions, TLS configuration. Removed: the statistics-refresh/large-cluster slowness claim and the "read-only" assertion about monitoring users.
Method: documentation only; no commands were run.
