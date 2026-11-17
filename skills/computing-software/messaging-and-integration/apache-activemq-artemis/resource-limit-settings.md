---
id: computing-software.messaging-and-integration.apache-activemq-artemis.resource-limit-settings
name: resource-limit-settings
category: computing-software
field: messaging-and-integration
product: apache-activemq-artemis
tags: [artemis,resource-limit-settings,max-sessions,max-queues,per-user-limits,activemq-artemis]
level: practitioner
status: docs-checked
description: "Cap how many sessions and queues a given user can create with resource-limit-settings max-sessions and max-queues in broker.xml."
sources:
  - https://github.com/apache/activemq-artemis/blob/main/docs/user-manual/resource-limits.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource limit settings

**Goal:** restrict what a particular authenticated user can create, beyond authentication and authorization.

## Configure
```xml
<resource-limit-settings>
   <resource-limit-setting match="myUser">
      <max-sessions>5</max-sessions>
      <max-queues>3</max-queues>
   </resource-limit-setting>
</resource-limit-settings>
```
Unlike `address-setting`, `match` here uses no wildcard syntax: it is a plain 1:1 mapping to a user name.

- `max-sessions`: how many sessions the matched user can create on the broker. Default `-1` (no limit).
- `max-queues`: how many queues the matched user can create. Default `-1` (no limit).

## Why sessions, not connections
In the Core API there is no separation between connection and session. A JMS `Connection` created with the Core JMS implementation creates a Core session that validates credentials and client ID, and each JMS `Session` creates another. Other protocols (STOMP, AMQP, MQTT) get a server-side session per network connection. So limiting sessions is the per-user limit on networked resources.

Raw TCP connections are tracked too and can be limited with the `connectionsAllowed` acceptor URL parameter, but they carry no credentials and so cannot be limited per user.

## Checked
2026-11-03. Confirmed against the Artemis user manual page resource-limits: XML, match semantics, max-sessions, max-queues, defaults and the sessions-versus-connections explanation. Removed: the Verify step.
Method: documentation only; no commands were run.
