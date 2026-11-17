---
id: computing-software.devops-ci-cd.atlantis.atlantis-execution-order-and-dependencies
name: atlantis-execution-order-and-dependencies
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [execution-order-group, depends-on, parallel-plan, parallel-apply, abort-on-execution-order-fail]
level: advanced
status: docs-checked
description: "Order project planning and applying with execution_order_group, depends_on and the parallel plan and apply options."
sources: ["https://www.runatlantis.io/docs/repo-level-atlantis-yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis execution order and dependencies

Atlantis can sequence or parallelise the projects in a pull request.

- `execution_order_group` (int, default `0`): projects are sorted by this value and lower groups run first. Groups apply only to a global `atlantis apply`, not to a single-project apply.
- `abort_on_execution_order_fail: true` (top-level): if a project in an earlier group fails, later groups are skipped.
- `depends_on` (since v0.20.0): lists project names that must be applied first. It works with single-project applies; applying a project whose dependency has not been applied returns an error that it cannot be applied until its dependencies are.
- `parallel_plan: true` and `parallel_apply: true` (top-level) run projects concurrently. The server flag `--parallel-pool-size` sets the maximum (default 15). The pool also governs `POST /api/plan` and `POST /api/drift/detect`; API applies still run one project at a time.

```yaml
version: 3
parallel_plan: true
parallel_apply: true
abort_on_execution_order_fail: true
projects:
- name: network
  dir: network
  execution_order_group: 1
- name: app
  dir: app
  execution_order_group: 2
  depends_on: [network]
```

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Repo Level atlantis.yaml, API Endpoints. Removed or fixed: generic closing paragraph.

Method: documentation only; no commands were run.
