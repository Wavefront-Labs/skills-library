---
id: computing-software.devops-ci-cd.concourse-ci.pipeline-schema-groups-display
name: pipeline-schema-groups-display
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [pipeline, schema, groups, display, user-data, var-sources, resource-types]
level: practitioner
status: docs-checked
description: "Write a Concourse pipeline top level: jobs, resources, resource_types, var_sources, groups with glob job patterns, display background and the user_data field kept by get-pipeline."
sources:
  - https://concourse-ci.org/docs/pipelines/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A pipeline is jobs and resources configured together, set from YAML through `fly set-pipeline` or the `set_pipeline` step; there is no GUI for configuring pipelines. The top-level keys are:

- `jobs` (required, at least one), `resources`, `resource_types` and `var_sources`.
- `groups`: tabs in the web UI that organise jobs. Groups have no functional effect. Once you add groups, every job must be in a group. The first group listed is the default view. A job may appear in several groups, and neighbours of the group's jobs also show for context. Job entries accept globs, for example `terraform-*`, `deploy-{dev,staging}` and `"*"`. Quote them, because `*`, `{` and `}` have special meaning in YAML.
- `display`: `background_image` (an http, https or relative URL) and `background_filter` (CSS filter, default `opacity(30%) grayscale(100%)`).
- `user_data`: arbitrary YAML of any type. It is not exposed during runtime, but it is preserved through the `fly set-pipeline` / `fly get-pipeline` cycle, and you can reference it with YAML anchors when setting pipelines. Any other unknown top-level keys are not preserved.

```yaml
groups:
  - name: develop
    jobs:
      - terraform-*
      - test
      - deploy-{dev,staging}
  - name: all
    jobs:
      - "*"
```

Pipeline names must satisfy the identifier schema from config basics.

## Checked

2026-11-04. Top-level keys, group rules, glob example, display fields and user_data behaviour confirmed on the Pipelines page.

Method: documentation only; no commands were run.
