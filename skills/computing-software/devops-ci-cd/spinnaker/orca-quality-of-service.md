---
id: computing-software.devops-ci-cd.spinnaker.orca-quality-of-service
name: orca-quality-of-service
category: computing-software
field: devops-ci-cd
product: spinnaker
tags: [orca, qos, buffering, executions, bufferpolicy, promotion, experimental]
level: sme
status: docs-checked
description: "Understand Orca's experimental QoS module: BufferStateSupplier, ordered BufferPolicy chain, BUFFERED executions and the ExecutionPromoter, and which executions it affects."
sources:
  - https://spinnaker.io/docs/guides/runbooks/orca-quality-of-service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The page marks QoS **experimental** (usable at Orca v6.71.0; Netflix runs it in learning mode and enables it judiciously during on-call events). It is disabled by default and manages how many executions are active at once.

**Scope.** The `orca-qos` module acts only on **newly created** executions, both pipelines and orchestrations. Once an execution has started it is outside QoS.

**Flow when enabled:**
1. On submission (UI, API or automated trigger) Orca emits a synchronous `BeforeExecutionPersist` event, which the `ExecutionBufferActuator` listens to.
2. A `BufferStateSupplier` decides whether new executions should go through QoS at all. If it returns false, the execution starts normally.
3. If true, the execution passes an ordered chain of `BufferPolicy` functions. Each returns `BUFFER` or `ENQUEUE`; **all** must return `ENQUEUE`, otherwise the execution gets status `BUFFERED` and its initialization is delayed.
4. Policies are pluggable. `EnqueueDeckOrchestrationBufferPolicy` is always on and always enqueues orchestrations that come from the UI, using a `force` flag that overrides other policies. A site could, for example, buffer low-criticality executions to leave capacity for critical ones (Netflix has an application criticality concept).
5. A buffered execution waits until the `ExecutionPromoter` moves it to `NOT_STARTED` and enqueues it. The promoter uses an ordered chain of `PromotionPolicy` functions each promotion cycle.

The promotion process runs by default on a 5-second interval on every Orca instance; the included naive promotion policy promotes the N oldest executions, and each policy result carries a logged human-readable reason.

**Configuration** (the page says this list may not be exhaustive):
- `qos.enabled` (default false) is the global flag; it does not disable the ExecutionPromoter.
- `qos.learningMode.enabled` (default true) always enqueues but logs and emits metrics for what QoS would have done.
- `pollers.qos.promoteIntervalMs` (default 5000).
- NaiveBufferPolicy: `qos.bufferPolicy.naive.enabled` (default true); it always buffers when enabled.
- ActiveExecutions supplier: set `qos.bufferingState.supplier` to `activeExecutions`; `qos.bufferingState.activeExecutions.threshold` (default 100); `pollers.qos.updateStateIntervalMs` (default 5000).
- KillSwitch supplier: set `qos.bufferingState.supplier` to `killSwitch`; `qos.bufferingState.killSwitch.enabled` (default false) turns QoS on, a config-only break-glass knob.
- NaivePromotionPolicy: `qos.promotionPolicy.naive.enabled` (default true) and `qos.promotionPolicy.naive.size` (default 1).

**Metrics:** `qos.executionsBuffered`, `qos.executionsEnqueued`, `qos.actuator.elapsedTime`, `qos.promoter.elapsedTime`, `qos.promoter.executionsPromoted`.

State is shared-nothing: each Orca instance keeps its own buffering state and runs its own pollers.

## Checked

2026-11-04. Experimental status, scope, the buffering and promotion flow, force flag and the criticality example were confirmed on the Orca Quality of Service page; the configuration, metrics and shared-nothing note were confirmed on the same page.

Method: documentation only; no commands were run.
