---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-step-dependencies
name: woodpecker-step-dependencies
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [depends-on, dag, parallel-steps]
level: practitioner
status: docs-checked
description: "Run Woodpecker steps in parallel with a depends_on dependency graph."
sources: ["https://woodpecker-ci.org/docs/usage/workflow-syntax", "https://woodpecker-ci.org/docs/usage/workflows"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker step dependencies

Steps run serially until one of them sets `depends_on`. From then on Woodpecker builds a directed acyclic graph: every step starts immediately unless it lists dependencies.

```yaml
steps:
  - name: build
    image: golang
    commands:
      - go build
  - name: test
    image: golang
    commands:
      - go test
  - name: deploy
    image: woodpeckerci/plugin-s3
    depends_on: [build, test]
```

Here `build` and `test` start together and `deploy` waits for both.

Rules:

- Setting `depends_on` on a single step makes all other steps without dependencies start immediately as well.
- An empty `depends_on: []` makes a step start at once, with no dependencies.
- Once any step uses `depends_on`, steps are looked up by name, so every step name in the workflow must be unique. Duplicate names are rejected.
- An entry can be an object with `optional: true`; the dependency is silently dropped if that step was filtered out by a `when` condition.

## Checked

2026-11-03. Confirmed against: workflow-syntax (depends_on, empty list, unique names) and workflows (optional step dependencies). Removed: an unsupported remark about parallel steps writing the same files.

Method: documentation only; no commands were run.
