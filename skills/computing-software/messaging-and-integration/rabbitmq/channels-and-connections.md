---
id: computing-software.messaging-and-integration.rabbitmq.channels-and-connections
name: channels-and-connections
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, channels-and-connections]
level: practitioner
status: docs-checked
description: "Use one long-lived TCP connection per process and a channel per thread or task; know when channel-level errors close the channel."
sources:
  - https://www.rabbitmq.com/docs/channels
  - https://www.rabbitmq.com/docs/connections
  - https://www.rabbitmq.com/docs/limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels and connections

**Goal:** Avoid connection churn and channel leaks.

## Steps
1. Connections are meant to be long-lived: do not open one per message or protocol operation. Open channels per thread or process and do not share a channel between them.
2. Limit channels per connection; most applications need a single-digit number per connection.
3. Close channels you no longer need; an operation on a closed channel raises an exception, and closing a connection closes its channels. The channels guide has a section on channel exceptions and what they mean.
4. Connections that publish can outpace the broker and be throttled by flow control; the connections guide has a Flow Control section.

## Failure modes
- Channel leaks: excessive channels use memory and Erlang processes on the node; the server-side `channel_max` setting limits channels per connection.

## Verify
- `rabbitmqctl list_connections name channels` and `rabbitmqctl list_channels` show counts per connection.

## Checked

2026-11-02. Confirmed in docs/channels, docs/connections, docs/limits: long-lived connections, channel per thread, single-digit guideline, resource use and leaks, channel_max, list_channels, flow control section; rabbitmqctl man page: connection info items. Removed: "one connection per process", separate publish/consume connections, and exact 404/406 reply-code meanings (not in pages read).
Method: documentation only; no commands were run.
