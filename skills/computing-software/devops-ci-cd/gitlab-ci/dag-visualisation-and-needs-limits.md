---
id: computing-software.devops-ci-cd.gitlab-ci.dag-visualisation-and-needs-limits
name: dag-visualisation-and-needs-limits
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, dag-visualization, needs-limit, job-dependencies-view, ci-needs-size-limit]
level: practitioner
status: docs-checked
description: "Inspect and debug DAG pipelines with the job dependencies view, know the 50-needs limit and where admins change it, and spot critical paths that stage ordering hides."
sources: ["https://docs.gitlab.com/ci/yaml/needs/", "https://docs.gitlab.com/ci/yaml/#needs", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/needs.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAG visualisation and needs limits

## 1. See the graph
On the pipeline details page select **Job dependencies**, then optionally toggle **Show dependencies**
to draw lines showing which jobs are linked. Use it to answer "why did deploy start before e2e finished?"
(it did not `need` e2e).

## 2. Limits
- Max jobs in a single job's `needs`: **50** on GitLab.com; the default is also 50 on Self-Managed and Dedicated, where an administrator can change it under the CI/CD limits in the Admin area.
- A `needs` entry that refers to a `parallel` job depends on every job it generates.
- You can refer to jobs in the same stage as the job you are configuring.

## 3. Reading critical path
- With `needs`, a job starts as soon as the jobs it lists finish, so pipeline duration follows the longest chain of needs rather than the sum of stages. Look for one slow early job that many jobs need and split it.
- A job without `stage:` uses the default `test` stage.
- `needs: []` jobs start as soon as the pipeline is created: good for lint and scanners that only need source code, wrong for anything that must follow a gate.

## 4. Gotchas
- A job with `needs` ignores stage ordering: a `deploy`-stage job can run before `test` stage jobs it does not need. Add the gate explicitly.
- Staged and `needs` jobs can be mixed in one pipeline; `needs:project` and `needs:pipeline` fetch artifacts or mirror status and do not create job dependencies.

## Verify
- [ ] Job dependencies view shows every deploy job connected to the test gate.
- [ ] No job's `needs` list exceeds the limit (the pipeline is created).

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/needs.md and doc/ci/yaml/_index.md: the Job dependencies view and Show dependencies toggle, the 50-job `needs` limit and where Self-Managed administrators change it, parallel jobs counting as all their generated jobs, same-stage references, `needs: []` behaviour, default `test` stage, and mixing staged and `needs` jobs. Removed the Rails console command, the version number for same-stage needs, `glab ci view`, the API and CI Lint tips, the cycles claim and the manual-job claim, none of which these pages state.

Method: documentation only; no commands were run.
