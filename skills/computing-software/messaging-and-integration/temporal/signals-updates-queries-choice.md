---
id: computing-software.messaging-and-integration.temporal.signals-updates-queries-choice
name: signals-updates-queries-choice
category: computing-software
field: messaging-and-integration
product: temporal
tags: [signals, updates, queries, message-passing, update-validator, workflow-messages]
level: practitioner
status: docs-checked
description: "Choose between Temporal Signals, Updates and Queries: write versus read, tracked versus fire-and-forget, validation, history cost and the read-after-state pattern."
sources:
  - https://docs.temporal.io/encyclopedia/workflow-message-passing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A workflow behaves like a stateful web service whose handlers react to messages and current state.

- Query: read request; reads current state but cannot block. Never adds Events to history and works on completed workflows.
- Signal: asynchronous write; you cannot await a response or error.
- Update: synchronous, tracked write; the sender can wait for the result or error.

Write requests, Signals when:
- the client wants to move on quickly;
- fire and forget is fine with no result or exception;
- the client does not depend on Worker availability;
- you do not want to cap messages processed concurrently by one workflow;
- latency does not matter.

Updates when:
- the client must track completion;
- it needs a result or exception without a Query;
- you want a Validator to vet the Update before it enters the workflow and history;
- you stay within the per-workflow concurrent Update limits (Cloud and self-hosted limits differ);
- the client wants low-latency end-to-end confirmation. An Update must wait for the Worker running the workflow to acknowledge it.

Read requests: prefer Query for efficiency. When you need a read once the workflow reaches some state, either poll with Queries or write the read as an Update, which is more efficient and lower latency but writes an Event to history if accepted.

Read/write requests: use an Update. If it must be asynchronous, send a Signal and then poll with a Query.

## Checked

2026-11-08. Read in full on the Workflow message passing page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
