---
id: computing-software.messaging-and-integration.rabbitmq.production-checklist
name: production-checklist
category: computing-software
field: messaging-and-integration
product: rabbitmq
tags: [rabbitmq, messaging, production-checklist, rmq-production]
level: practitioner
status: docs-checked
description: "Apply the production checklist: remove guest, TLS, resource limits, monitoring, backups of definitions, sizing."
sources:
  - https://www.rabbitmq.com/docs/production-checklist
  - https://www.rabbitmq.com/docs/definitions
  - https://www.rabbitmq.com/docs/backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Production checklist

**Goal:** Reach a defensible baseline.

## Steps
1. Delete the default `guest` user; use TLS; use a separate vhost per application in multi-tenant setups.
2. Use an odd number of nodes (3, 5, 7); three nodes tolerate one failure. Use fast local SSD or NVMe storage.
3. Allow at least 50K open file descriptors; set `vm_memory_high_watermark` deliberately (recommended relative range 0.4 to 0.7).
4. Import definitions at deployment time and keep exports of them (definitions can be exported and imported as JSON). Set up monitoring.

## Failure modes
- Some configurations make sense for development but not production.

## Verify
- `rabbitmq-diagnostics check_if_node_is_quorum_critical` before taking a node down for maintenance.

## Checked

Date: 2026-11-02. Confirmed on the Production Deployment Guidelines, Backup guide and Upgrade guide: guest, TLS, vhosts, node counts, SSD/NVMe, 50K descriptors, watermark range, definitions, quorum-critical check. Removed: "use quorum queues", "5 nodes" as a specific recommendation, Prometheus, "test failover".

Method: documentation only; no commands were run.
