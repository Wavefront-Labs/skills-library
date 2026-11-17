---
id: computing-software.messaging-and-integration.rabbitmq.logging-configuration
name: logging-configuration
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, logging-configuration]
level: practitioner
status: docs-checked
description: "Configure log levels, outputs and categories (connection, channel, queue) for diagnosis."
sources:
  - https://www.rabbitmq.com/docs/logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging configuration

**Goal:** Get useful logs.

## Steps
1. `log.file.level = info` (the file output level; default is info), `log.console = true` (default false) and `log.connection.level = info` for the connection category.
2. Rotate with `log.file.rotation.date`, `log.file.rotation.size` and `log.file.rotation.count`.
3. Raise the level at runtime with `rabbitmqctl set_log_level debug` (the guide shows `rabbitmqctl -n <node> set_log_level debug`).

## Failure modes
- Debug level is verbose; use it temporarily.

## Verify
- Open a connection and find it in the log.

## Checked

2026-11-02. Confirmed in docs/logging: log.file.level and default, log.console and default, log.connection.level, rotation keys, set_log_level. Removed: logrotate recommendation (not in the page).
Method: documentation only; no commands were run.
