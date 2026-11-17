---
id: computing-software.devops-ci-cd.nomad.autopilot-config
name: autopilot-config
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, autopilot-config, autopilot, cleanup-dead-servers, last-contact-threshold, max-trailing-logs, server-stabilization-time, operator-write, cli]
level: advanced
status: docs-checked
description: "Tune Nomad Autopilot with nomad operator autopilot set-config: cleanup-dead-servers, last-contact-threshold, max-trailing-logs, server-stabilization-time."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/autopilot/set-config.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad operator autopilot set-config

Changes the live Autopilot configuration for the server cluster. Needs the `operator:write` capability with ACLs on. Output is `Configuration updated!`; exit status shows success.

```
nomad operator autopilot set-config -cleanup-dead-servers=false
nomad operator autopilot set-config -last-contact-threshold=200ms -max-trailing-logs=250
```
(The second line shows flag syntax only; the numeric values are examples, not recommendations.)

## Flags
- `-cleanup-dead-servers=[true|false]` - automatically remove dead servers when new servers join successfully.
- `-last-contact-threshold <duration>` - how long a server may go without leader contact before it is unhealthy (duration such as `200ms`).
- `-max-trailing-logs <n>` - how many log entries a server may trail the leader by before it is unhealthy.
- `-server-stabilization-time <duration>` - minimum time a server must be healthy before being added to the cluster (for example `10s`); only effective if all servers run Raft protocol version 3 or higher.
- Also: `-disable-upgrade-migration=[true|false]` (avoid promoting new servers until a migration can happen), `-redundancy-zone-tag` (the `redundancy_zone` value) and `-upgrade-version-tag` (the `upgrade_version` used for upgrade migrations; blank means the Nomad version).

## Checked

2026-11-03. Confirmed against the Nomad 1.10 operator autopilot set-config command page: the flags, the 200ms and 10s duration examples, operator:write, the Configuration updated! output. Removed: the Enterprise-only label and the get-config/health inspection section.

Method: documentation only; no commands were run.
