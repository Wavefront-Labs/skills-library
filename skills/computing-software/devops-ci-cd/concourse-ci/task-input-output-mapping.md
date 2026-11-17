---
id: computing-software.devops-ci-cd.concourse-ci.task-input-output-mapping
name: task-input-output-mapping
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [task-step, input-mapping, output-mapping, artifacts, reusable-tasks, generic-tasks]
level: practitioner
status: docs-checked
description: "Reuse one generic task several times in a plan with input_mapping and output_mapping, renaming its inputs and outputs to the concrete artifact names in the build."
sources:
  - https://concourse-ci.org/docs/steps/task/
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/across/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A reusable task config often declares generic names such as `main` and `dev`. The task step can bind those to concrete artifacts.

- `input_mapping`: map from task input names to artifact names in the build plan.
- `output_mapping`: map from task output names to the names registered in the build plan afterwards.

This lets the same task file be used more than once in one plan. The documented example maps inputs `main` and `dev` to the artifacts `repo` and `repo-dev`:

```yaml
plan:
  - in_parallel:
      - get: repo
      - get: repo-dev
      - get: ci
  - task: create-outputs
    input_mapping:
      main: repo
      dev: repo-dev
    output_mapping:
      main: repo
      dev: repo-dev
    file: ci/tasks/generic-outputs.yml
  - in_parallel:
      - put: repo
        params:
          file: repo/version
      - put: repo-dev
        params:
          file: repo-dev/version
```

The task config declares `inputs` and `outputs` named `main` and `dev`, and writes `main/version` and `dev/version`. Because the outputs are mapped back to `repo` and `repo-dev`, the following `put` steps can reference those names directly.

The same mappings combine with an `across` step, where the mapping keys and values can use the across var, for example `((.:pipeline)): ci`.

## Checked

Checked 2026-11-09 against the raw docs source of the Task Step page and the Across Step Modifier page (both read in full): mapping semantics, the generic-outputs example and the across example using `((.:pipeline))` as a mapping key all match.

Method: docs-checked 2026-11-09 against concourse docs task step and across pages (github.com/concourse/docs source); documentation only, no commands were run.
