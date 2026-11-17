---
id: computing-software.devops-ci-cd.nomad.node-drain
name: node-drain
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, node-drain, drain, deadline, ignore-system, force, no-deadline, keep-ineligible, decommission, migration, cli]
level: practitioner
status: docs-checked
description: "Drain a Nomad client with nomad node drain: per-job-type behaviour, one hour default deadline, -force, -no-deadline, -ignore-system, -keep-ineligible."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/node/drain.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad node drain

Toggles drain mode: no new allocations are placed on the node and existing ones are migrated away.

```
nomad node drain -enable -deadline 30m -m "node maintenance" <node-id-prefix>
nomad node drain -disable <node>
nomad node drain -enable -self
```
One of `-enable` or `-disable` is required. Give a node ID or prefix, or `-self`. ACL: `node:write`.

## What happens by job type
- **service**: migrated following each job's `migrate` block until the deadline (`computing-software.devops-ci-cd.nomad.migrate-block`). Not counted as reschedules; prior reschedule attempts are not propagated.
- **batch / sysbatch**: allowed to finish until they complete or the deadline hits; not replaced.
- **system**: stopped last by default, not replaced.

## Options
- `-deadline` (default 1 hour) - after this, remaining allocations are removed regardless of `migrate`.
- `-no-deadline` - never force removal.
- `-force` - remove everything immediately, including system jobs and CSI plugins unless `-ignore-system`. Unsafe for CSI node plugins unless volumes are detached externally (for example the VM is being terminated).
- `-ignore-system` - leave system job allocations (and CSI plugins) running.
- `-keep-ineligible` - when disabling a drain, keep the node ineligible (cancel a drain without letting work return).
- `-detach` (return immediately), `-monitor` (watch without changing drain), `-m` (message, stored as `message` or `cancel_message`), `-meta key=value` (repeatable), `-yes`.

## Gotchas
- Ctrl-C only stops monitoring; it does **not** cancel the drain. Cancel with `-disable`.
- Disabling a drain restores eligibility by default.
- Draining multiple nodes: first run `nomad node eligibility -disable` on all of them, then drain, so evacuated allocations do not land on a node that is about to drain (`computing-software.devops-ci-cd.nomad.node-eligibility`).
- Check progress with `nomad node status`.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 node drain command page: behaviour by job type, every listed option, deadline default of 1 hour, Ctrl-C behaviour, multi-node advice, node:write. Nothing removed.

Method: documentation only; no commands were run.
