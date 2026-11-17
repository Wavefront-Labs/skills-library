---
id: computing-software.rpa-and-low-code.n8n.choose-branching-patterns
name: choose-branching-patterns
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, source-control, branches, environments, review, upgrades]
level: intro
status: docs-checked
description: "Choose how n8n instances map to Git branches: multi-branch environments, shared branch for upgrade testing, and one reviewing instance that switches branches."
sources:
  - https://docs.n8n.io/administer/use-source-control-and-environments/choose-branching-patterns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: pick the instance-to-branch layout.

- **Multiple instances, multiple branches**: development and production each on their own branch. Push from development, open a pull request to the production branch, then pull to the production instance.
- **Multiple instances, one branch**: same workflows, tags and variables everywhere. Push from development, pull into production. Also useful to test a new n8n version: stand up a new instance on the shared branch while production stays on the old version until you trust the upgrade.
- **One instance, multiple branches**: the instance owner can switch the connected branch, handy for reviewing: authors push to their own branches from their own instances and a review instance loads each in turn. n8n does not clean up the instance when you switch, so workflows from every branch loaded accumulate.
- One instance, one branch: the simplest pattern.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/administer/use-source-control-and-environments/choose-branching-patterns

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Removed the Settings > Environments path (not on the page read).

Method: documentation only; no commands were run.
