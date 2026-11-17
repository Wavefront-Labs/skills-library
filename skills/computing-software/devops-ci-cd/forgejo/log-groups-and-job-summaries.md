---
id: computing-software.devops-ci-cd.forgejo.log-groups-and-job-summaries
name: log-groups-and-job-summaries
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [log-grouping, job-summaries, endgroup, markdown-summary]
level: practitioner
status: docs-checked
description: "Fold log output with ##[group] markers and render Markdown job summaries from steps."
sources:
  - https://forgejo.org/docs/latest/user/actions/advanced-features/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Log grouping: print `##[group]Headline` to start an expandable section and `##[endgroup]` to end it. Groups can be nested. Example inside a step: echo `##[group]Headline`, then lines that stay hidden until expanded, then `##[endgroup]`. The `##[endgroup]` lines are not shown but still count in line numbers, and text after the last group is never hidden.

Job summaries: each step can render extra Markdown. A job summary is the composition of the summaries from each step, rendered on top of the log output as soon as a step appends content. Mermaid and KaTeX are supported. Each step can append up to 1MiB of Markdown; surplus content is truncated automatically.

Related feature, run prioritisation: by default jobs run in arrival order, but a whole workflow run can be marked prioritised from Options > Prioritize run in the run list, and cleared with Do not prioritize run. Prioritised runs execute before others, in arrival order among themselves. It is best-effort, for example it has no effect on a run already running, and the order is not exposed via the HTTP API or webhooks.

## Checked

2026-11-04. Confirmed against the Forgejo Actions advanced features page (Grouping of log messages, Workflow Run Prioritization, Job Summaries): the group markers, nesting, line numbering, 1MiB step limit, Mermaid and KaTeX, and the prioritisation behaviour. Nothing removed.

Method: documentation only; no commands were run.
