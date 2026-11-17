---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-workflow-dependencies
name: woodpecker-workflow-dependencies
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [depends-on, optional-dependencies, workflow-ordering]
level: advanced
status: docs-checked
description: "Order Woodpecker workflows with depends_on, optional dependencies and run-on-failure."
sources: ["https://woodpecker-ci.org/docs/usage/workflows", "https://woodpecker-ci.org/docs/usage/workflow-syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker workflow dependencies

Workflows are independent unless you set `depends_on` at the top level of a workflow file. A workflow waits until all its dependencies finished successfully.

```yaml
steps:
  - name: deploy
    image: debian:stable-slim
    commands:
      - echo deploying

depends_on:
  - lint
  - build
  - test
```

The name is the file name without path, leading dots and the `.yml`/`.yaml` extension; `.woodpecker/.lint.yaml` is referenced as `lint`.

To run a workflow even after failures, set a status filter:

```yaml
when:
  - status: [success, failure]
```

In a monorepo, workflows with `when: path` may be filtered out, which would block a deploy workflow forever. Mark those dependencies optional:

```yaml
depends_on:
  - check-a
  - name: check-b
    optional: true
```

An optional dependency is enforced only if that workflow is part of the pipeline; otherwise it is ignored. The same syntax works for steps. Without `optional`, a workflow depending on a skipped workflow is excluded as well.

## Checked

2026-11-03. Confirmed against: workflows (depends_on, name rule, status filter, optional dependencies) and workflow-syntax (skipped workflows). Removed: nothing.

Method: documentation only; no commands were run.
