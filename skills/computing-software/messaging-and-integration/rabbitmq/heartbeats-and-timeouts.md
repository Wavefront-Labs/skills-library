---
id: computing-software.messaging-and-integration.rabbitmq.heartbeats-and-timeouts
name: heartbeats-and-timeouts
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, heartbeats-and-timeouts]
level: practitioner
status: docs-checked
description: "Set AMQP heartbeats (default 60s) and TCP keepalives to detect dead connections and survive load balancers."
sources:
  - https://www.rabbitmq.com/docs/heartbeats
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heartbeats and timeouts

**Goal:** Avoid ghost connections and idle drops.

## Steps
1. The heartbeat timeout is negotiated at connect time; RabbitMQ suggests 60 seconds by default and the client must request heartbeats. Java, .NET and Erlang clients use the smaller of the two non-zero values.
2. Heartbeats also keep connections active through proxies and load balancers: at 30 seconds, traffic flows about every 15 seconds, enough for most proxy defaults. Avoid very low values, which cause false positives.
3. TCP keepalives are a separate mechanism; enable with `tcp_listen_options.keepalive = true`.

## Failure modes
- Disabling heartbeats (0 on both sides) removes dead-peer detection unless TCP keepalives are tuned on every host.

## Verify
- After two missed heartbeats the peer is considered unreachable and the TCP connection is closed.

## Checked

Date: 2026-11-02. Confirmed on the Heartbeats guide and Configuration page. Removed: the 30-60 second recommendation as stated, "match load balancer idle timeout above the interval", the cable-pull test.

Method: documentation only; no commands were run.
