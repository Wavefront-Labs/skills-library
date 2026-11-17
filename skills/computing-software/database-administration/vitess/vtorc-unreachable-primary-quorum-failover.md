---
id: computing-software.database-administration.vitess.vtorc-unreachable-primary-quorum-failover
name: vtorc-unreachable-primary-quorum-failover
category: computing-software
field: database-administration
product: vitess
tags: [vtorc, quorum, emergency-reparent, track-shard-tablet-health, split-brain, vttablet-unreachable]
level: sme
status: docs-checked
description: "Enable VTOrc quorum-confirmed failover for a primary whose vttablet is unreachable but whose MySQL runs, with the vttablet and VTOrc flags, tuning defaults and split-brain caveat."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-basic/vtorc/
  - https://vitess.io/docs/25.0/reference/vtorc/ui_api_metrics/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Normally VTOrc declares a primary dead from MySQL health, so a primary whose `vttablet` crashed while `mysqld` keeps running leaves a shard with no serving primary and no automatic recovery. Starting in v25 VTOrc can run EmergencyReparentShard in this case, gated by a quorum so VTOrc never acts on its own connectivity problem. It proceeds only if the primary's vttablet is unreachable to VTOrc and a quorum of the shard's REPLICA/RDONLY tablets independently report it unreachable, using existing `Ping` and `FullStatus` RPCs. The analysis is `PrimaryTabletUnreachableByQuorum`; opt-in on both sides:

- vttablet: `--track-shard-tablet-health` (peers ping the primary; cadence and timeout `--shard-tablet-health-interval`, default 1s).
- VTOrc: `--emergency-reparent-on-primary-tablet-unreachable`.

Tuning flags on VTOrc: `--shard-tablet-health-quorum-fraction` (1.0, unanimous), `--shard-tablet-health-quorum-min-observers` (1), `--shard-tablet-health-failure-threshold` (3 consecutive ping failures), `--shard-tablet-health-freshness` (15s; must exceed `--instance-poll-time`, ideally 2-3x).

Behaviours: graceful vttablet shutdown stamps a shutdown time and the path fails closed, so deliberate maintenance never reparents. The denominator is the shard's REPLICA/RDONLY count from the topology, so down replicas count against the majority; with a single observer the decision rests on that observer plus VTOrc's check, so raise min-observers if you want more. The old primary's MySQL keeps running until its vttablet returns, so use a semi-sync durability policy; with `none`, clients bypassing vtgate could cause split brain.

Observe it via logs, the recovery audit message and `/api/shard-tablet-health-quorum`.

## Checked

2026-11-04. Flags, defaults, behaviours and observability confirmed in the quorum failover section of the VTOrc user guide; endpoint description on the VTOrc UI, API and Metrics page.

Method: documentation only; no commands were run.
