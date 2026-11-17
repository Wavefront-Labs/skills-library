---
id: computing-software.messaging-and-integration.rabbitmq.rabbitmqctl
name: rabbitmqctl
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, rabbitmqctl, rmq-cli]
level: intro
status: docs-checked
description: "Use rabbitmqctl for node, user, vhost, policy and queue management and know its Erlang cookie requirement."
sources:
  - https://www.rabbitmq.com/docs/man/rabbitmqctl.8
  - https://www.rabbitmq.com/docs/cli
  - https://www.rabbitmq.com/docs/shovel-dynamic
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rabbitmqctl

**Goal:** Administer a node from the shell.

## Steps
1. Common commands: `rabbitmqctl status`, `list_queues`, `list_connections`, `list_users`, `set_policy`, `add_user`.
2. Target another node with `-n` (`--node`); the tool authenticates with a shared secret, the Erlang cookie, which must match the node's.
3. `--formatter json` gives machine-readable output (the shovel guide uses `shovel_status --formatter=json`).

## Failure modes
- "Authentication failed ... please check the Erlang cookie" on the CLI is a cookie mismatch.

## Verify
- `rabbitmqctl status` returns the node info.

## Checked

Date: 2026-11-02. Confirmed on the rabbitmqctl man page, CLI Tools guide (cookie, `--node`, authentication failures) and Shovel guide (`--formatter`). Removed: the claim that the failure message always means a cookie mismatch beyond what the CLI guide states.

Method: documentation only; no commands were run.
