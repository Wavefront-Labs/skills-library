---
id: computing-software.devops-ci-cd.concourse-ci.set-pipeline-step
name: set-pipeline-step
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [set-pipeline-step, self-updating, vars, var-files, instance-vars, team, archive]
level: practitioner
status: docs-checked
description: "Use the set_pipeline step: self-updating pipelines, file, vars versus instance_vars versus var_files, setting another team's pipeline from main, and auto-archiving."
sources:
  - https://concourse-ci.org/docs/steps/set-pipeline/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`set_pipeline: name` configures a pipeline from a YAML file in an earlier artifact (`file: examples/pipelines/hello-world.yml`). It is created unpaused in the current team. `set_pipeline: self` makes a pipeline update its own config. A common job fetches the repo with `trigger: true` and then runs the step, keeping the pipeline in sync with source control without manual `fly set-pipeline`.

Fields:
- `vars`: template variables for interpolation only; they do not become part of the identifier.
- `instance_vars`: also interpolated, but they identify an instanced pipeline, so several `set_pipeline` steps with the same name and different `instance_vars` form one instance group. Instanced pipelines need `CONCOURSE_ENABLE_PIPELINE_INSTANCES=true` on versions below v8.
- `var_files`: list of `.yml` files passed like `--load-vars-from`; later files override earlier ones.
- `team`: only the `main` team may set another team's pipeline; any other team using it errors unless it names its own team.

Neither `vars` nor `instance_vars` propagate to tasks defined by `task` step `file`; pass `vars` on the task step too if you need them.

Pipelines set this way are tied to the job and are automatically archived when a successful build of that job no longer sets them, when the job is removed from its pipeline (use `old_name` to rename), or when the job's pipeline is archived or destroyed. So set all still-wanted pipelines in every build, rather than one per build.

## Checked

2026-11-04. Fields, auto-archive rules and the team restriction confirmed on the Set Pipeline Step page.

Method: documentation only; no commands were run.
