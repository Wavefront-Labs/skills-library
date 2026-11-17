---
id: computing-software.systems-network-administration.incus.instance-lifecycle
name: instance-lifecycle
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, start, stop, delete, rebuild, protection, instance-state, operations]
level: practitioner
status: docs-checked
description: "Start, stop, delete and rebuild Incus instances, protect against deletion with security.protection.delete, and the state API calls."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance lifecycle

- `incus start <name>` (add `--console` to attach); fails if missing or already running.
- `incus stop <name>`; fails if missing or not running.
- API: `PUT /1.0/instances/<name>/state` with `{"action":"start"}` or `{"action":"stop"}`. The reply carries an operation ID checkable at `/1.0/operations/<id>`.
- `incus delete <name>` needs the instance stopped and removes its snapshots too. `DELETE /1.0/instances/<name>` in the API.
- Guard against deletion: set `security.protection.delete=true`, or alias `incus alias add delete "delete -i"` to force a prompt.
- Rebuild wipes and reinitialises the root disk but keeps configuration. Requires a stopped instance with no snapshots:
  - `incus rebuild <image> <name>`
  - `incus rebuild <name> --empty`
  - API: `POST /1.0/instances/<name>/rebuild` with a `source` (alias, server, protocol `simplestreams`) or `{"type":"none"}`.

## Checked

2026-11-04: confirmed against the Incus manage-instances how-to (start/stop errors, state API calls and operation ID, delete requirements, `security.protection.delete`, the delete alias, rebuild rules and API). Nothing removed.

Method: documentation only; no commands were run.
