---
id: computing-software.devops-ci-cd.dagger.debug-observability
name: debug-observability
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, debugging, observability, tui, traces, opentelemetry, terminal, breakpoints]
level: practitioner
status: docs-checked
description: "Debug Dagger workflows with --interactive, Terminal() breakpoints, TUI verbosity flags and Dagger Cloud Traces built on OpenTelemetry."
sources: [https://docs.dagger.io/0.21/introduction/features/observability, https://docs.dagger.io/0.21/getting-started/quickstarts/basics, https://docs.dagger.io/0.21/getting-started/quickstarts/ci/, https://docs.dagger.io/0.21/introduction/features/shell]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug and observe Dagger workflows

Goal: find out why a pipeline failed or is slow (Dagger 0.21 docs).

## Drop into a shell at the failure point

Run the function with `--interactive` (the docs' example: `dagger call --interactive foo`, where the function deliberately does `cat /FOO` after writing `/foo`). Dagger opens an interactive terminal at the point of failure with context intact; no code changes or explicit breakpoints are needed.

## Explicit breakpoints

Add `Terminal()` to a Container in code; each one opens a session at that point:
```go
return dag.Container().
	From("alpine:latest").
	Terminal().
	WithExec([]string{"sh", "-c", "echo hello world > /foo"}).
	Terminal()
```
In Dagger Shell, chain `| terminal` (the shell page shows `terminal --cmd=/bin/bash`).

## Terminal UI (TUI)

The CLI renders a live DAG similar to `git log --graph`: a red X or green check per call, durations, errors at the top below the progress report, and a final snapshot of output. It shows state (cached or pending), duration, CPU, network and memory usage. Verbosity: `-v` keeps finished spans visible, `-vv` reveals internal and encapsulated spans, `-vvv` reveals sub-100ms spans; add `--debug` to `dagger call` for more detail.

## Traces in Dagger Cloud

Create an account with `dagger login`; later runs print a link to a Trace. A Trace is one function invocation (local or CI) with a flame graph, searchable logs, breadcrumbs, separate error highlighting, and in-progress/cancelled indicators. Traces are grouped by Git branch and reference; CI traces with missing Git metadata are "orphaned" and ungrouped. Agent prompts and tool calls are traced too.

## OpenTelemetry

Dagger telemetry is OpenTelemetry: each function call is a trace, operations are spans, and one span can emit several effects (`withDirectory()` loads a directory then creates a new one). Custom resource attributes can be added via the standard `OTEL_RESOURCE_ATTRIBUTES` environment variable. User code that integrates with OpenTelemetry shows related spans in the TUI.

Related: `computing-software.devops-ci-cd.dagger.dagger-shell-basics`.

## Checked

2026-11-07

Read in full from the docs source: introduction/features/observability.mdx, introduction/features/shell.mdx, getting-started/quickstarts/basics and quickstarts/ci. Added the quickstart and shell pages as sources (they hold the `dagger login` and terminal examples). Replaced the unsupported `--cmd=bash` mention with the shell page's `terminal --cmd=/bin/bash`.

Method: documentation only; no commands were run.
