---
id: computing-software.messaging-and-integration.rabbitmq.export-definitions
name: export-definitions
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, export-definitions, rmq-definitions]
level: practitioner
status: docs-checked
description: "Export and import definitions (users, vhosts, queues, exchanges, bindings, policies) as JSON for backup and cloning."
sources:
  - https://www.rabbitmq.com/docs/definitions
  - https://www.rabbitmq.com/docs/http-api-reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Export and import definitions

**Goal:** Back up and replicate topology.

## Steps
1. `rabbitmqctl export_definitions defs.json`; `rabbitmqctl import_definitions defs.json` (export is the only option that does not need the management plugin).
2. Load at boot with the core `load_definitions` setting in `rabbitmq.conf` (a file path); definitions in the file do not overwrite anything already in the broker.
3. Exported user records contain password hashes and the hashing function; treat the file as sensitive.
4. Definitions cover exchanges, queues, bindings, users, virtual hosts, permissions, topic permissions and parameters, not messages.

## Failure modes
- Importing into a broker that already has entities can conflict; import at boot into a blank node for clean results.

## Verify
- Diff exports before and after.

## Checked

2026-11-02. Confirmed in docs/definitions and docs/http-api-reference: export/import commands, load_definitions, no overwrite on boot import, password hashes, contents list. Removed: nothing load-bearing; reworded the live-import conflict warning.
Method: documentation only; no commands were run.
