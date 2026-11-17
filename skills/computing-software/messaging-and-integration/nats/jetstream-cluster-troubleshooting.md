---
id: computing-software.messaging-and-integration.nats.jetstream-cluster-troubleshooting
name: jetstream-cluster-troubleshooting
category: computing-software
field: messaging-and-integration
product: nats
tags: [troubleshooting, nats-server-report, server-request, system-account, debug-logging]
level: practitioner
status: docs-checked
description: "Diagnose JetStream cluster problems with nats account/server commands, debug/trace logging and a required system user."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/configuration/clustering/jetstream_clustering/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a checklist of commands for diagnosing a misbehaving JetStream cluster.

Tips from the page:
1. Read nats-server logs. By default only warnings and errors appear; turn on debug with `-D` or trace with `-DV` (or the equivalent config options).
2. Ensure at least one system user is configured in the `$SYS` account (`{ $SYS { users } }`), because most server commands go through the system account.

Command families:
- Account: `nats account info` verifies JetStream is enabled on the account.
- Basic server: `nats server ls`, `nats server ping`, `nats server info`, `nats server check` (health check).
- Reports: `nats server report connections`, `accounts`, `jetstream`.
- Requests: `nats server request jetstream`, `subscriptions`, `variables`, `connections`, `routes`, `gateways`, `leafnodes`, `accounts`.
- Cluster: `nats server cluster step-down` (force a new meta leader) and `nats server cluster peer-remove` (remove a server from a JetStream cluster).
- Experimental: `nats traffic` monitors NATS traffic.

Gotcha: server commands rely on a system user being configured, so set that up before an outage; the page assumes working knowledge of JetStream concepts and the nats CLI.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
