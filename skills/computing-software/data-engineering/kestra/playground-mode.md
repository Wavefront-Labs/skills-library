---
id: computing-software.data-engineering.kestra.playground-mode
name: playground-mode
category: computing-software
field: data-engineering
product: kestra
tags: [playground, ui, iterative-development, cached-outputs, dag]
level: intro
status: docs-checked
description: "Build Kestra flows iteratively in Playground mode: run one task at a time on cached upstream outputs, and know what resets results and what does not."
sources:
  - https://kestra.io/docs/ui/playground
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Playground lets you run one task at a time in the UI, like a Jupyter notebook: run an extraction, inspect output, then test transformations without rerunning extraction.

- Each task has a Play button that runs only that task, reusing cached outputs of upstream tasks already played.
- Run all tasks and Run all downstream tasks run several in sequence.
- It needs a DAG structure: a task cannot run until its upstream tasks have been played.
- Up to 10 recent Playground runs are kept; older ones are purged.
- Playground runs do not appear in the regular execution list.

A fresh run starts when you change a task before the one you are running, the flow `inputs`, `labels` or `variables`.

Caveat: Playground tracks only the flow definition. Changes to namespace files, KV entries, secrets, or an external system a task reads do not reset reused results, so outputs may be stale. Use Run all tasks for a fresh run.

## Checked

2026-11-04. Confirmed against the Kestra Playground docs page: per-task Play with cached upstream outputs, Run all tasks and Run all downstream tasks, the DAG requirement, 10 retained runs, exclusion from the execution list, the reset triggers and the stale-result caveat. Nothing removed.

Method: documentation only; no commands were run.
