---
id: computing-software.messaging-and-integration.rabbitmq.rabbitmq-conf
name: rabbitmq-conf
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, rabbitmq-conf, rmq-config]
level: practitioner
status: docs-checked
description: "Configure the broker with rabbitmq.conf (sysctl format), advanced.config and environment variables."
sources:
  - https://www.rabbitmq.com/docs/configure
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rabbitmq.conf

**Goal:** Configure reproducibly.

## Steps
1. Use `rabbitmq.conf` (new-style format) for most settings, `advanced.config` (Erlang terms) for the few settings it cannot express, and `rabbitmq-env.conf` for environment variables.
2. Find the config files a node uses with `rabbitmq-diagnostics status` (Config files section).
3. Changes to `rabbitmq.conf` and `advanced.config` take effect after a node restart.

## Failure modes
- The classic `.config` format predates RabbitMQ 3.7.0; use the new format for ordinary settings.

## Verify
- `rabbitmq-diagnostics environment` prints the effective configuration (user values merged into defaults).

## Checked

2026-11-02. Confirmed in docs/configure: file roles, status command and Config files section, restart rule, classic format before 3.7.0, `rabbitmq-diagnostics environment`. Real error fixed: the skill said `rabbitmqctl environment`; the guide documents `rabbitmq-diagnostics environment`.
Method: documentation only; no commands were run.
