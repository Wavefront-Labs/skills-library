---
id: computing-software.devops-ci-cd.gitlab-ci.stageless-pipelines-with-needs
name: stageless-pipelines-with-needs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, stageless-pipeline, needs, dag]
level: practitioner
status: docs-checked
description: "Build stageless GitLab pipelines where needs alone defines order: implicit test stage, needs: [] for immediate start, visualisation and the pitfalls of mixing styles."
sources: ["https://docs.gitlab.com/ci/yaml/needs/", "https://docs.gitlab.com/ci/yaml/#needs", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/needs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stageless pipelines (needs without stages)

A job can `needs:` a job in the **same** stage, so you can drop `stages:`
entirely. Every job without `stage:` lands in the default `test` stage and ordering comes from `needs`.

```yaml
build:
  script: make build
  artifacts: { paths: [bin/] }
unit:
  needs: [build]
  script: make test
lint:
  needs: []          # start immediately, no dependencies
  script: make lint
image:
  needs: [build]
  script: make image
deploy:
  needs: [unit, image]
  script: make deploy
  rules: [{ if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH' }]
```

## Rules of thumb
- `needs: []` starts the job as soon as the pipeline is created. Without `needs`, a job waits for all jobs in earlier stages; in a stageless file with one stage that is nothing, so be explicit.
- Artifacts: a job with `needs` downloads artifacts only from the jobs listed in `needs` (set `artifacts: false` on an entry to skip it).
- `.pre`/`.post` still work for setup/cleanup jobs.
- Max 50 jobs in `needs` per job by default.

## Pitfalls
- Mixing stages and needs: a job with no `needs` waits for whole earlier stages. One forgotten
  `needs` re-serialises the pipeline.
- The pipeline graph groups by stage; use **Job dependencies** (toggle **Show dependencies**) to see the DAG.
- If a needed job is excluded by `rules`, the pipeline might fail to be created unless the entry uses `optional: true` (for example `needs: [{job: image, optional: true}]`).

## Verify
- [ ] The pipeline is created for push and merge request events.
- [ ] The dependency view shows the intended DAG.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md and doc/ci/yaml/needs.md: same-stage `needs`, `needs: []` starting at pipeline creation, `needs` limiting artifact downloads to listed jobs and `needs:artifacts`, default `test` stage, the 50-job limit, `.pre` and `.post`, the Job dependencies view, and `needs:optional`. Removed the 14.2 version number, the `ci_max_needs` name, the manual-job blocking claim and the quoted error text, and the `make` commands are placeholders rather than documented behaviour.

Method: documentation only; no commands were run.
