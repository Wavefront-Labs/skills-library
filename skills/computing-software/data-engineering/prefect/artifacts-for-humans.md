---
id: computing-software.data-engineering.prefect.artifacts-for-humans
name: artifacts-for-humans
category: computing-software
field: data-engineering
product: prefect
tags: [artifacts, markdown-artifact, link-artifact, ui, reporting]
level: intro
status: docs-checked
description: "Publish human-readable outputs from Prefect flows and tasks as link, markdown, progress, image and table artifacts shown in the UI."
sources:
  - https://docs.prefect.io/v3/concepts/artifacts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: surface results in the Prefect UI.

Artifacts are persisted outputs designed for human consumption, stored in Prefect Cloud or the Prefect server and rendered in the UI. They annotate flow and task runs. Five types exist: links, markdown, progress, images, tables.

Functions named: `create_link_artifact()` and `create_markdown_artifact()`.

Behaviour:
- Each call creates a separate artifact that appears individually in the UI.
- Unlike `print()`, calls cannot be concatenated into one report. Build the whole message string first, then pass it to `create_markdown_artifact()`.

Use cases the page lists:
- progress indicators for long-running tasks
- debugging, for example seeing which flow run last updated an artifact, or linking to storage locations such as S3 buckets
- data quality checks across a pipeline and tracking artifact versions over time
- documentation and sample data with descriptions of why the data matters

The concept page gives no size, count or rate limits and does not document the function parameters; see the Prefect how-to guide on producing artifacts.

## Checked
2026-11-08. Confirmed against the Artifacts concept page: storage and UI rendering, the five types, create_link_artifact and create_markdown_artifact, one artifact per call, and the listed use cases. Removed a guessed how-to URL that was not read.
Method: documentation only; no commands were run.
