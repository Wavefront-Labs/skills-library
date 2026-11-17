---
id: computing-software.messaging-and-integration.temporal.workflow-definition-determinism
name: workflow-definition-determinism
category: computing-software
field: messaging-and-integration
product: temporal
tags: [workflow-definition, determinism, nondeterminism, replay, commands, workflow-type]
level: practitioner
status: docs-checked
description: "Write Temporal workflow definitions that replay safely: which API calls emit Commands, which changes are safe, and how nondeterminism errors arise."
sources:
  - https://docs.temporal.io/workflow-definition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a workflow definition replayable.

Parameters: take a single object (struct, dataclass, class) rather than several arguments. Adding an optional field leaves the signature alone so running executions survive; type-safe client calls usually accept one argument; the Web UI can only send one input.

Determinism: on every execution the code must make the same Workflow API calls in the same order for the same input. Calls that produce Commands must not be added, removed or reordered without versioning: starting or cancelling a Timer; scheduling or cancelling Activities (local too); starting or cancelling Child Workflows; signalling or cancelling signals to external workflows; scheduling or cancelling Nexus operations; ending the execution (complete, fail, cancel, continue-as-new); `Patched`/`GetVersion`; upserting Search Attributes or Memos; `SideEffect`/`MutableSideEffect`.

Mechanism: on replay, each emitted Command is compared with the Event at the same position in history (an Activity call yields `ScheduleActivityTask`, which must meet `ActivityTaskScheduled` with the same Activity name). A mismatch returns a non-deterministic error.

Safe edits: Timer duration (but changing to or from 0 is unsafe in Java, Python and Go; -1 in .NET), Activity or Child Workflow options and timeouts, arguments for signalling an external workflow, adding a Signal handler for a Signal never sent, calls that produce no Commands such as `workflow.GetInfo`.

Intrinsic nondeterminism: never branch on the local clock or random numbers; use the SDK's time, random and side-effect APIs, whose results are stored in history. Put API calls, database access and LLM calls in Activities.

## Checked

2026-11-08. Read in full on the Temporal Workflow Definition page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
