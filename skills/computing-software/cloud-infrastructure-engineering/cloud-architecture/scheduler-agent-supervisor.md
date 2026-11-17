---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.scheduler-agent-supervisor
name: scheduler-agent-supervisor
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, scheduler-agent-supervisor, workflow-recovery, distributed-workflow, state-store, supervisor-pattern]
level: advanced
status: docs-checked
description: "Implement the scheduler agent supervisor pattern: scheduler drives steps, agents call services, supervisor finds expired steps in durable state and retries or compensates."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/scheduler-agent-supervisor", "https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduler agent supervisor

Coordinates a multistep distributed task so the whole operation succeeds or is undone, recovering from transient faults, longer-lasting faults and process failures.

## Roles (Azure Architecture Center)
- **Scheduler**: runs the steps as a workflow and records each step's state (not started, running, completed) in a durable state store, with a **complete-by** time. It talks to Agents by asynchronous request/response messaging, often queues, and passes the complete-by time and retry allowance.
- **Agent**: wraps a call to one remote service or resource, with its own error handling and retries inside the complete-by time. It passes a stable identifier across retries so downstream can deduplicate, and must not start new side effects after the deadline.
- **Supervisor**: runs periodically, scans the state store for steps still "running" with an expired complete-by time (a timeout and a failure look the same by design), and arranges recovery. It only requests recovery; the Scheduler and Agents carry it out. It does not restart failed workers (hosting infrastructure does that) and need not know business logic.

The Scheduler ignores late responses and Agents do not attempt workflow recovery themselves.

## Recovery options
1. Extend complete-by and ask the Scheduler to retry the step. Steps must therefore be idempotent. Keep a per-step retry count in the state store; past a threshold, wait longer before retrying.
2. Ask the Scheduler to undo the whole task with a compensating transaction. The compensation log needs ordering (compensations run in reverse order of completed steps) as well as durability. The state store must distinguish compensation in progress, completed and failed rather than one Error state.

## Multiple instances
Several Schedulers, Agents or Supervisors may run. Supervisors must coordinate so they do not recover the same step; the Leader Election pattern is one way. If the Supervisor fails, another instance resumes; if it runs on a schedule a new instance starts at the next interval.

## Considerations from the page
- Hard to implement; test every failure mode, including fault injection.
- Retry amplification: independent retries at the Agent, runtime, client library, messaging and Supervisor layers multiply calls to a failing dependency. Make the Scheduler own an end-to-end retry budget and cap the other layers.
- Admission control: the pattern does not limit in-flight work, so a failing downstream grows the backlog silently. Use a bounded queue, a cap on concurrent tasks or rejection when backlog is high.
- State store and compensation log are first-class durable assets and inherit the data classification of what they track.
- Submitting a task is usually a dual write (business record plus state record) with no shared transaction; options are a durable orchestration with compensating delete, the Transactional Outbox pattern or a stable task ID that makes writes repeatable.
- Version workflow logic and persisted state, since tasks can span deployments.
- Choose Supervisor cadence against typical step duration and acceptable detection delay: too slow delays recovery, too fast loads the state store.
- Decide what each role emits and which thresholds alert.

## When not to use
When the task does not call remote services or resources: no distributed failure surface, so overhead without benefit.

## Managed workflow engines
Step Functions (Amazon States Language) provides Catch and Retry on Task, Parallel and Map states, `TimeoutSeconds` and `HeartbeatSeconds` (the error `States.HeartbeatTimeout` when a task misses its heartbeat window), and by default a state error fails the whole execution. `States.Timeout` is reported when a state or execution exceeds `TimeoutSeconds`. Azure's own example implements the pattern with Durable Functions, Service Bus and Cosmos DB. Use an engine unless it does not fit.

## Verify
- [ ] Kill an Agent mid-step: the Supervisor detects the expired complete-by and recovery happens within the agreed window.
- [ ] A step run twice produces one side effect.
- [ ] A failed compensation is visible as its own state.

## Checked
2026-11-08, documentation only.
Confirmed against: Azure Architecture Center, Scheduler Agent Supervisor pattern (read through the Example section's opening); AWS Step Functions Developer Guide, Error handling.
Removed as unconfirmed: Temporal and Google Workflows claims, optimistic-concurrency ETag advice for the state store, the claim that Step Functions retries "heartbeats" beyond the error names above, and the Durable Functions feature list (the overview page read was only a landing page).
Method: documentation only; no commands were run.
