---
id: computing-software.devops-ci-cd.gitlab-ci.when-manual-delayed-and-on-failure-jobs
name: when-manual-delayed-and-on-failure-jobs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, when-delayed, start-in, when-on-failure, when-manual, manual-confirmation, blocking-manual-jobs]
level: practitioner
status: docs-checked
description: "Control when jobs run with when: on_success, on_failure, always, manual and delayed with start_in; blocking vs optional manual jobs and manual_confirmation prompts."
sources: ["https://docs.gitlab.com/ci/yaml/#when", "https://docs.gitlab.com/ci/jobs/job_control/#create-a-job-that-must-be-run-manually", "https://docs.gitlab.com/ci/jobs/job_control/#run-a-job-after-a-delay"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# when: manual, delayed, on_failure

## 1. Values
| when | Runs |
|---|---|
| `on_success` (default) | no job in earlier stages failed (jobs with `allow_failure: true` and skipped manual jobs count as successful) |
| `on_failure` | at least one job in an earlier stage failed |
| `always` | regardless of status |
| `manual` | only when someone clicks play / calls the API |
| `delayed` + `start_in` | after a countdown (`30 minutes`, `1 day`; minimum 1 second, maximum 1 week) |
| `never` | only in `rules` or `workflow:rules`: do not run the job |

## 2. Manual: blocking vs optional
```yaml
deploy-prod:
  stage: deploy
  script: ./deploy.sh prod
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual            # inside rules: allow_failure defaults to false -> BLOCKING
  manual_confirmation: "Deploy to production?"     # custom confirmation message (GitLab 17.1+)
  environment: production
```
- `when: manual` at job level (not in rules) defaults to `allow_failure: true`: the pipeline
  succeeds without anyone clicking ("skipped" manual job is fine).
- Inside `rules` (default `allow_failure: false`), or with explicit `allow_failure: false`, the job is **blocking**: the pipeline stops at its stage until the job is run and shows a **blocked** status, and merge requests with *Pipelines must succeed* enabled cannot merge. Use blocking for gates, optional for convenience jobs.
- Who can run it: you need permission to merge to the assigned branch; use protected branches and protected environments to restrict manual deployments.

## 3. Delayed
```yaml
rollout-rest:
  stage: deploy
  when: delayed
  start_in: 30 minutes
  script: ./promote-canary.sh
```
The timer starts when the previous stage completes, and only if that stage passes. A stage that includes a delayed job does not progress until the delayed job finishes. **Unschedule** stops the timer so the job can only be run manually; select **Run** afterwards to start it immediately. Classic use: staged rollout with a human able to stop it.

## 4. on_failure for notifications/cleanup
```yaml
notify-failure:
  stage: .post
  when: on_failure
  script: ./notify.sh "$CI_PIPELINE_URL"
```

## Gotchas
- A blocking manual job in an early stage stops everything after it; scope it with `rules`.
- `start_in` only works with `when: delayed` (any other `when` makes the configuration invalid); when the job uses `rules`, `start_in` and `when` must both be inside the rule or you get a validation error.
- To pass variables to a manual job, select the job name in the pipeline view and use the **Run job** form.

## Verify
- [ ] The default-branch pipeline shows **blocked** until the production deploy is run; merge request pipelines are not blocked.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md (`when`, `manual_confirmation`, `start_in`) and doc/ci/jobs/job_control.md (manual job types, blocked status, who can run, delayed jobs, unschedule, minimum one second and maximum one week). Removed the claim that `on_failure` with `needs` considers only needed jobs, the claim that start_in outside delayed is ignored (the docs say the configuration is invalid), and anything about the countdown display. Note: `when: manual` defaults to `allow_failure: true` outside `rules` and `false` inside `rules`, as the docs state.

Method: documentation only; no commands were run.
