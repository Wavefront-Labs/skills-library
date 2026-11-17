---
id: computing-software.devops-ci-cd.gitlab-ci.workflow-name-and-pipeline-naming
name: workflow-name-and-pipeline-naming
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, workflow-name, pipeline-name, ci-pipeline-name, workflow-rules-variables, auto-cancel]
level: intro
status: docs-checked
description: "Name pipelines with workflow:name (dynamic, via workflow:rules:variables) so scheduled, tag and MR pipelines are recognisable, plus workflow auto_cancel settings."
sources: ["https://docs.gitlab.com/ci/yaml/#workflowname", "https://docs.gitlab.com/ci/yaml/#workflowauto_cancelon_new_commit", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# workflow:name and pipeline naming

## 1. Dynamic names
```yaml
variables:
  PIPELINE_NAME: "Branch pipeline: $CI_COMMIT_REF_NAME"
workflow:
  name: $PIPELINE_NAME
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      variables: { PIPELINE_NAME: "Nightly $SCHEDULE_NAME" }
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      variables: { PIPELINE_NAME: "MR !$CI_MERGE_REQUEST_IID: $CI_MERGE_REQUEST_TITLE" }
    - if: $CI_COMMIT_TAG
      variables: { PIPELINE_NAME: "Release $CI_COMMIT_TAG" }
    - when: always
```
- The name is available to jobs as `CI_PIPELINE_NAME`. Leading and trailing spaces are removed, and an empty result means the pipeline gets no name.
- Names longer than 255 characters are truncated after variable expansion (truncation is a GitLab 19.6 behaviour behind the `ci_truncate_workflow_name` flag, enabled by default).
- Values can be a string, CI/CD variables, or both.
- `workflow:rules:variables` become default variables in all jobs, including `trigger` jobs that forward variables downstream, so use unique variable names or `inherit:variables`.
- Set `SCHEDULE_NAME` as a variable on each schedule to tell nightly pipelines apart.
- The Pipelines API accepts a `name` query parameter to return pipelines with the specified name.

## 2. auto_cancel (same block)
```yaml
workflow:
  auto_cancel:
    on_new_commit: interruptible     # conservative (default) | interruptible | none
    on_job_failure: all              # all | none
```
`on_new_commit: interruptible` cancels only jobs with `interruptible: true` when a new commit starts a new pipeline; `conservative` cancels the pipeline only if no `interruptible: false` job has started; `none` cancels nothing.
`on_job_failure: all` cancels the pipeline and all running jobs as soon as one job fails; `none` cancels nothing.

## Gotchas
- Quote values that contain `: ` so the YAML stays valid.
- When no `workflow:rules` entry matches, the pipeline does not run; keep a final catch-all rule such as `- when: always` if every event should create a pipeline.

## Verify
- [ ] The pipelines list shows "Nightly ..." for scheduled runs and "MR !123: ..." for merge requests.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md (`workflow:name`, `workflow:rules`, `workflow:auto_cancel:on_new_commit`, `workflow:auto_cancel:on_job_failure`), doc/ci/variables/predefined_variables.md (`CI_PIPELINE_NAME` and the variables used in the example) and doc/api/pipelines.md (`name` filter). Removed the claim that only global variables are allowed in the name, and the advice about avoiding `on_job_failure: all` on the default branch. The predefined variables used in the example (`CI_COMMIT_REF_NAME`, `CI_MERGE_REQUEST_IID`, `CI_MERGE_REQUEST_TITLE`, `CI_COMMIT_TAG`, `CI_PIPELINE_SOURCE`) were confirmed in the predefined variables page.

Method: documentation only; no commands were run.
