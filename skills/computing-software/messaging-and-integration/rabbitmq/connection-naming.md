---
id: computing-software.messaging-and-integration.rabbitmq.connection-naming
name: connection-naming
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, connection-naming]
level: intro
status: docs-checked
description: "Set a connection name so operators can identify which app owns each connection."
sources:
  - https://www.rabbitmq.com/docs/connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection naming

**Goal:** Trace connections to apps.

## Steps
1. Set the `connection_name` field in the client capabilities (client properties) table, using your client library's option for it.
2. Pick a descriptive naming convention such as service plus instance.

## Failure modes

## Verify
- Check that the name appears in the management UI or in `rabbitmqctl list_connections`.

## Checked

Date: 2026-11-02. Confirmed in the Connections guide (docs/connections): the `connection_name` field of the client capabilities table. Removed as not stated there: the specific naming format and the Connections-tab claim is kept only as a check to perform.

Method: documentation only; no commands were run.
