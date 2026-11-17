---
id: computing-software.messaging-and-integration.temporal.message-handler-patterns
name: message-handler-patterns
category: computing-software
field: messaging-and-integration
product: temporal
tags: [message-handlers, signal-handler, update-handler, update-validator, idempotency, all-handlers-finished, workflow-initializer]
level: advanced
status: docs-checked
description: "Write safe Temporal Signal, Update and Query handlers: concurrency, initializers, waiting, all handlers finished, idempotency, validators and exception effects."
sources:
  - https://docs.temporal.io/handling-messages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Concurrency: each workflow runs on one thread in a loop that processes messages in arrival order, then advances the main method. Handlers that block (Activities, waits) interleave with the main method and each other, so make them reentrant; guard with the SDK's workflow-safe mutex or semaphore. Synchronous handlers that never block run atomically.

Initialise state first: messages can reach handlers before the main method runs (Signal-with-Start, a backlogged Task Queue, messages arriving just after Continue-As-New). Except in Go and TypeScript, use a constructor marked as Workflow Initializer taking the same arguments as the main method; it cannot block, so make handlers wait for an init flag. In Go and TypeScript, register handlers only after initialisation.


Finish handlers before completing or continuing as new: await the All Handlers Finished condition. Setting Handler Unfinished Policy to Abandon silences warnings, but clients awaiting those Updates get Not Found.

Idempotency: the server dedupes Updates by Update ID (a UUID unless you set it). Signals need your own key in the input. With Continue-As-New, dedupe Updates in workflow code because Update ID dedup is per run. Retried client calls are deduped by request IDs automatically.

Update Validator: non-blocking read that accepts (Update enters history) or rejects (workflow never sees it).

Exceptions (not Go): in Signals, Application Failure, Activity Failure or Child Workflow Failure fails the whole workflow; any other exception fails the Workflow Task. In Updates, validator exceptions, those failures, or Application Failure fail only the Update.

## Checked

2026-11-08. Read in full on the Handling Signals, Queries, & Updates page: every concrete claim (names, events, rules, fields) matches the page.

Method: documentation only; no commands were run.
