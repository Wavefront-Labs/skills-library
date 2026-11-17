---
id: computing-software.data-engineering.apache-flink.restart-strategies-and-failover
name: restart-strategies-and-failover
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-deployment, restart-strategy, exponential-delay, failure-rate, fixed-delay, failover-strategy, region-failover, fault-tolerance]
level: practitioner
status: docs-checked
description: "Configure Flink restart strategies (exponential-delay, fixed-delay, failure-rate) and failover regions so transient failures self-heal while permanent ones fail fast and alert."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/task_failure_recovery/
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink restart strategies and failover

**Goal:** jobs recover by themselves from transient errors (lost TaskManager, broker blip) and stop loudly on permanent errors (bad record, bug) instead of restart-looping forever.

## 1. Strategies
```yaml
# exponential backoff (the default when checkpointing is enabled and no strategy is set)
restart-strategy.type: exponential-delay
restart-strategy.exponential-delay.initial-backoff: 1 s
restart-strategy.exponential-delay.max-backoff: 5 min
restart-strategy.exponential-delay.backoff-multiplier: 2.0
restart-strategy.exponential-delay.reset-backoff-threshold: 1 h     # healthy this long → backoff resets
restart-strategy.exponential-delay.jitter-factor: 0.1
restart-strategy.exponential-delay.attempts-before-reset-backoff: 10  # default is infinite; finite → job fails after 10 consecutive retries
```
```yaml
# failure-rate: tolerate N failures per interval
restart-strategy.type: failure-rate
restart-strategy.failure-rate.max-failures-per-interval: 3
restart-strategy.failure-rate.failure-rate-interval: 5 min
restart-strategy.failure-rate.delay: 10 s
```
```yaml
# fixed-delay: N attempts total
restart-strategy.type: fixed-delay
restart-strategy.fixed-delay.attempts: 5
restart-strategy.fixed-delay.delay: 30 s
```
`none` — fail immediately (tests, batch where the orchestrator retries).
Per job in code: `RestartStrategyOptions` on the job's configuration; a job-level strategy overrides the cluster default.

## 2. Choosing
- Long-running streaming: exponential-delay with a finite attempt budget or failure-rate. Unlimited restarts hide a poison record that fails every time — the job "runs" while making no progress.
- Make permanent errors non-retriable at the source: catch parse errors and route bad records to a side output/DLQ instead of throwing.
- After the strategy gives up, the job goes FAILED → alert. If you run the Kubernetes operator, decide whether it should redeploy a failed job — usually no, so a human looks.

## 3. Failover strategy (what restarts)
- `jobmanager.execution.failover-strategy: region` (default) restarts only the **pipelined region** containing the failed task.
- `full` restarts all tasks in the job; rarely needed.

## 4. Recovery speed
- Restart replays from the last checkpoint: shorter checkpoint intervals = less replay but more overhead.
- **Local recovery** (`state.backend.local-recovery: true`) restores from a local copy on the same TaskManager when possible — much faster for large RocksDB state.
- Spare TaskManagers / slots (`slotmanager.redundant-taskmanager-num`) avoid waiting for a new pod.

## 5. Diagnose restart loops
Flink UI > Job > Exceptions shows the history with root causes and the failing task/TM. Typical loops: deserialization of a bad record, external sink rejecting writes, OOM in one subtask (skewed key), checkpoint storage permission errors.

## Verify
- [ ] Killing a TaskManager pod → job recovers within the backoff window.
- [ ] A permanently failing record → job fails after the configured budget and an alert fires.
- [ ] Job restarts are graphed and alerted.

## Checked
2026-10-31. Confirmed against the Flink stable Task Failure Recovery page and the configuration page: all `restart-strategy.*` keys, exponential-delay as the default when checkpointing is on, `attempts-before-reset-backoff` (default infinite), `jobmanager.execution.failover-strategy` values `region` (default) and `full`, `state.backend.local-recovery`, `slotmanager.redundant-taskmanager-num`. Removed: the operator restart key, the `numRestarts` metric name and the all-to-all region claim (not on these pages).
Method: documentation only; no commands were run.
