---
id: computing-software.devops-ci-cd.gitlab-ci.pre-and-post-stages
name: pre-and-post-stages
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, pre-post-stages, dot-pre-dot-post, pipeline-setup-teardown]
level: intro
status: docs-checked
description: "Use the built-in .pre and .post stages for setup and teardown jobs that always run first and last, including their limits with rules, needs and failure handling."
sources: ["https://docs.gitlab.com/ci/yaml/#stage-pre", "https://docs.gitlab.com/ci/yaml/#stage-post", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `.pre` and `.post` stages

By default `.pre` is the first stage and `.post` the last; you do not have to list them in `stages:`.
Useful for included templates that must not depend on the project's stage names.

## 1. Examples
```yaml
validate-config:
  stage: .pre
  script: echo "check required variables"

report-to-dashboard:
  stage: .post
  when: always              # run after failures too
  script: echo "push pipeline metrics"
```

## 2. Rules
- If a pipeline contains only jobs in the `.pre` or `.post` stages, it does not run; at least one job in another stage is required.
- User-defined stages run after `.pre` and before `.post`.
- `when` works as usual: `on_success` (the default) skips the job when an earlier job failed; use `when: always` for reporting or cleanup and `when: on_failure` for alerts.
- Jobs with `needs: []` and jobs in `.pre` all start as soon as the pipeline is created, so `needs: []` jobs do not wait for `.pre`. Add an explicit `needs` on the setup job when order matters.
- A pipeline execution policy can define `.pipeline-policy-pre`, which runs before `.pre`, and `.pipeline-policy-post`, which runs after `.post`.

## 3. Good uses
- Fail fast on missing variables or a bad version string before the other stages start.
- `.post`: metrics push, environment cleanup, notifications.
- Avoid heavy work in `.pre`: it delays every stage-based job.

## Verify
- [ ] The pipeline graph shows `.pre` jobs first and `.post` last; the reporting job runs on a failed pipeline.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md (`stage: .pre`, `stage: .post`, `when`, `needs`): default positions, no need to declare them in `stages`, pipelines with only `.pre` or `.post` jobs do not run, the `needs: []` interaction, `when` semantics, and the `.pipeline-policy-pre` and `.pipeline-policy-post` stages. Removed the quoted error text, the claim that the order cannot be changed, the 40-job figure and the notification specifics, which the page does not state.

Method: documentation only; no commands were run.
