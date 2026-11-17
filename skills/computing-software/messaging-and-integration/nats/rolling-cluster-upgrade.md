---
id: computing-software.messaging-and-integration.nats.rolling-cluster-upgrade
name: rolling-cluster-upgrade
category: computing-software
field: messaging-and-integration
product: nats
tags: [upgrade, rolling-restart, healthz, downgrade, lame-duck]
level: practitioner
status: docs-checked
description: "Upgrade or downgrade a NATS cluster one node at a time using lame duck mode and waiting for /healthz 200."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/upgrading_cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace server versions in a cluster without an outage.

Procedure, repeated for every node one at a time:
1. Stop the server by putting it in lame duck mode (`nats-server --signal ldm`), which evicts clients gradually.
2. Replace the binary or Docker image with the new version.
3. Restart the server.
4. Wait until the `/healthz` endpoint returns `HTTP 200 OK` before moving on to the next node.

The health check needs the monitoring port enabled (`-m` or `http_port`).

Downgrading: the server is tested per release, but if a release regresses your workload you can revert. The downgrade path is identical: swap the binary and do a rolling restart. The support policy covers the current release and one patch release before it.

Gotchas: never restart several nodes together; do not skip the health check; make sure clients reconnect cleanly (see lame duck mode).

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
