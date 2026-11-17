---
id: computing-software.rpa-and-low-code.n8n.control-concurrency
name: control-concurrency
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, concurrency, production-limit, queue, workers, executions]
level: practitioner
status: docs-checked
description: "Limit concurrent production executions in self-hosted n8n with N8N_CONCURRENCY_PRODUCTION_LIMIT, its exclusions, queued-execution behaviour and queue-mode interplay."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/control-concurrency
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: stop too many simultaneous production executions from thrashing the event loop. In regular mode n8n has no limit by default.

Enable: `export N8N_CONCURRENCY_PRODUCTION_LIMIT=20`. Executions over the limit wait in a FIFO queue until capacity frees.

## Rules
- Applies only to production executions started by a webhook or trigger node. Not manual, sub-workflow, error or CLI-started executions.
- Queued executions cannot be retried; cancelling or deleting one removes it from the queue.
- At startup n8n resumes queued executions up to the limit and re-enqueues the rest.
- Monitor via logs (executions added and released); with the limit enabled the project or workflow executions tab shows active count and limit.

## Queue mode
Per-worker concurrency uses the `--concurrency` flag, but `N8N_CONCURRENCY_PRODUCTION_LIMIT` controls both mechanisms: in queue mode n8n uses it when set to a value other than `-1`, otherwise the flag or its default.

## Evaluations
Evaluation test runs have their own limit by license tier (Community/Pro 1, Business 3, Enterprise 5), overridden by `N8N_CONCURRENCY_EVALUATION_LIMIT`.

n8n Cloud concurrency is documented separately.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/scaling/control-concurrency

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
