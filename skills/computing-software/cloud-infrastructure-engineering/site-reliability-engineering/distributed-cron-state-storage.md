---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.distributed-cron-state-storage
name: distributed-cron-state-storage
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cron-state-storage, distributed-cron-state, distributed-cron, paxos, leader-election, scheduler-ha]
level: advanced
status: docs-checked
description: "Store distributed cron state as the SRE Book describes: replicated launch intents in a consensus store, leader-only launching, and recovery of partial launches after failover."
sources: ["https://sre.google/sre-book/distributed-periodic-scheduling/", "https://sre.google/sre-book/managing-critical-state/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed cron state storage

SRE Book: Google's distributed cron runs replicas that use Paxos to agree on state; only the **leader**
launches jobs. State must survive leader failover so the new leader knows what was and was not launched.

## What state to keep
- Per job: schedule, last scheduled launch time, last successful launch, in-progress launch.
- **Launch intent before action**: before launching, the leader writes "about to launch job X for
  scheduled time T" to the replicated store; after launching, writes "launched X for T". This two-step
  record lets a new leader detect a **partial launch** (intent written, completion not).

## Handling partial failure on failover
A new leader seeing an unfinished intent cannot know if the launch happened. Options from the book:
- Make external operations **idempotent** (e.g. deterministic job names derived from job + scheduled time
  so re-launching the same name is a no-op or detectable).
- **Look up the state** of the external system (does a job with that name exist?) before re-launching.
A job name derived from the job and its scheduled time makes the lookup and dedup straightforward
(this naming is a suggestion, not from the book).

## Storage choices
- The book's two options: a small replicated store inside the cron service itself, or an external
  distributed storage. It rejects a distributed filesystem for the live state because small writes there are
  expensive and slow; the state is small.
- Keep the Paxos log from growing forever by snapshotting. Google keeps logs and snapshots on replica local
  disk and also backs snapshots up to a distributed filesystem, since snapshots are the most critical state
  (losing logs loses only the state since the last snapshot).

## Leader election
Only the leader launches jobs and modifies shared state; in Google's cron the Fast Paxos leader is the cron
leader. A deposed leader must stop launching immediately (see `leader-election-implementation`).

## Off-the-shelf equivalents
The Kubernetes CronJob docs say a CronJob may occasionally create two Jobs or none, so Jobs should be
idempotent; do not assume exactly-once launching from a scheduler.

## Gotchas
- A "last run" kept only on each replica's local disk, outside the replicated state, can cause double or
  skipped launches after failover; the book notes a trade-off between double launch and skipped launch.
- Time zone and DST: store scheduled times in UTC; render to local only for display.

## Verify
- [ ] Kill the scheduler leader mid-launch in staging: job launched exactly once (by name) after failover.
- [ ] Restore of scheduler state from snapshot tested.

## Checked
2026-11-01. Confirmed in the SRE Book chapter Distributed Periodic Scheduling with Cron (Paxos replicas, single leader, two synchronisation points per launch, idempotent external operations, state lookup, snapshots and log growth, snapshot backup to a distributed filesystem, double versus skipped launch trade-off) and the Kubernetes CronJob page (may create two Jobs or none). Removed: etcd, ZooKeeper, Consul, Airflow and Temporal statements, the Kubernetes Job-name hash claim, and the instruction to store snapshots only on a distributed filesystem, which the book contradicts.
Method: documentation only; no commands were run.
