---
id: computing-software.devops-ci-cd.gitlab-ci.optional-needs-for-conditional-jobs
name: optional-needs-for-conditional-jobs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, needs-optional, optional-needs, needs-not-in-pipeline, conditional-dag]
level: practitioner
status: docs-checked
description: "Use needs with optional: true so a job can depend on jobs that rules sometimes exclude, avoiding pipeline creation errors for jobs that were not added."
sources: ["https://docs.gitlab.com/ci/yaml/#needsoptional", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# needs: optional

**Error this fixes:** an error similar to `'job1' job needs 'job2' job, but it was not added to the pipeline`
(the exact wording is in the keyword reference): the pipeline is not created when a needed job was removed by `rules`.

## 1. Pattern
```yaml
build-docs:
  rules:
    - changes: [docs/**/*]
  script: make docs

build-app:
  script: make app

deploy:
  needs:
    - build-app
    - job: build-docs
      optional: true          # wait for it and take its artifacts IF it exists
  script: ./deploy.sh
```
- Job present: `deploy` waits for it (and downloads its artifacts, since `artifacts` defaults to `true`).
- Job absent: the need is ignored and `deploy` starts when its other needs are met.

## 2. Things to know
- If the `needs` section contains only optional jobs and none are in the pipeline, the job starts immediately, the same as `needs: []` (usually fine, sometimes surprising).
- If the needed job is present, the job waits for it to complete before starting.
- `optional` defaults to `false`; with `false` a missing needed job stops the pipeline from being created.
- You cannot use `needs:optional` together with `needs:parallel:matrix`; it can be combined with `needs:pipeline:job` to need a job that sometimes does not exist in a parent or another child pipeline.
- The script must cope with missing artifacts when the optional job is absent.
- Alternative when the dependency is truly mandatory: put matching `rules` on both jobs so they appear and disappear together.

## Verify
- [ ] A pipeline where `build-docs` is excluded is still created and `deploy` runs after `build-app`.
- [ ] A pipeline with docs changes shows `deploy` waiting on `build-docs` in the dependency graph.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md (`needs`, `needs:optional`): the three behaviours when a needed job is present, absent, or all needs are optional and absent, the default `optional: false` and the error wording, and the restriction with `needs:parallel:matrix`. Removed the exact error text from the old heading, the claim that a present-but-failed optional need blocks the job, the `!reference` advice and the shell snippet, which the page does not cover.

Method: documentation only; no commands were run.
