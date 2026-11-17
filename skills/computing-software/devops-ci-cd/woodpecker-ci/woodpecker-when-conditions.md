---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-when-conditions
name: woodpecker-when-conditions
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [when, conditions, conditional-steps]
level: practitioner
status: docs-checked
description: "Write Woodpecker `when` blocks and understand how list entries and sub-conditions combine."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/linter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker `when` conditions

A step runs if at least one entry of its `when` list is true. An entry is true only if all of its sub-conditions are true.

```yaml
steps:
  - name: prettier
    image: woodpeckerci/plugin-prettier
    when:
      - event: pull_request
        repo: test/test
      - event: push
        branch: main
```

This step runs for a pull request in `test/test`, or for a push to `main`. Filters inside one entry are ANDed; separate list entries are ORed.

Available filters: `repo`, `branch`, `event`, `cron`, `ref`, `status`, `platform`, `matrix`, `instance`, `path` and `evaluate`.

Each filter accepts a single value or a list (`event: [push, tag, deployment]`).

Notes from the docs:

- A `branch` condition is not applied to tags.
- A `branch` condition also matches pull requests whose target branch is that branch; add an `event` filter to limit it to pushes.
- The linter warns when a `when` item has no `event` filter, because new events added later would also trigger the step. Give every item an `event`.

The same `when` block can be placed at the top level of the file to skip a whole workflow; there all conditions must be true.

## Checked

2026-11-03. Confirmed against: workflow-syntax (when, branch, event, workflow-level when) and linter (event filter warning). Removed: nothing.

Method: documentation only; no commands were run.
