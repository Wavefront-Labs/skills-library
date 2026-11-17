---
id: computing-software.data-engineering.dagster.run-queue-priority
name: run-queue-priority
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, run-queue, dagster-priority, tag-concurrency-limits, prioritization, backfills]
level: advanced
status: docs-checked
description: "Order Dagster queued runs with the dagster/priority tag and see how tag_concurrency_limits change launch order."
sources:
  - https://docs.dagster.io/deployment/execution/customizing-run-queue-priority
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Customizing run queue priority

The run queue is FIFO by default. All runs have priority `0`; higher priority launches first; ties keep submission order. Negative priorities are allowed, useful to de-prioritize sets of runs such as backfills.

## Set priority
Use the `dagster/priority` tag on definitions or via the Launchpad **Edit tags** button. The value must be an integer given as a string: `"1"`, `"-1"`.

## With concurrency limits
A run blocked by a tag concurrency limit does not block runs submitted after it. Instance setting:

```yaml
concurrency:
  runs:
    tag_concurrency_limits:
      - key: 'team'
        limit: 1
```
Submit A (`team: docs`), B (`team: docs`), C (untagged): A launches, B is skipped while A runs, C launches, B launches after A finishes. Order becomes A, C, B.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/deployment/execution/customizing-run-queue-priority

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: the QueuedRunCoordinator requirement (not stated on the page).

Method: documentation only; no commands were run.
