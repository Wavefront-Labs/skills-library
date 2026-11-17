---
id: computing-software.devops-ci-cd.gitlab-ci.scheduled-pipelines-and-trigger-tokens
name: scheduled-pipelines-and-trigger-tokens
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, scheduled-pipelines, pipeline-schedules, cron, schedule-owner, schedule-variables, ci-pipeline-source-schedule, nightly-builds, pipeline-triggers, trigger-token, pipelines-api, run-pipeline-api, glab-ci-run, webhook-trigger, external-trigger, pipeline-schedule-api, take-ownership, schedule-timezone, rules-schedule, inactive-schedule, pipeline-run-variables]
level: practitioner
status: docs-checked
description: "Run GitLab pipelines on a schedule or from outside: pipeline schedules (cron, owner permissions, variables), rules on $CI_PIPELINE_SOURCE, trigger tokens vs the pipelines API."
sources: ["https://docs.gitlab.com/ci/pipelines/schedules/", "https://docs.gitlab.com/ci/triggers/", "https://docs.gitlab.com/api/pipelines/", "https://docs.gitlab.com/api/pipeline_schedules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled pipelines and trigger tokens

**Goal:** nightly/weekly jobs that run reliably under the right identity, and a safe way
for external systems to start pipelines with parameters.

## 1. Pipeline schedules
Build > Pipeline schedules > New schedule: interval pattern (preconfigured or custom cron
such as `0 2 * * 1-5`), target branch or tag, inputs, and variables. Rules:
- The creator becomes the schedule **owner**; the pipeline runs with the owner's
  permissions and can use protected environments. Creating one needs the Developer,
  Maintainer or Owner role, and a verified primary email; for protected branches the owner
  needs merge permission on the target branch.
- If the owner is blocked or removed from the project, the schedule becomes **Inactive**.
  A Maintainer or Owner restores it with **Take ownership**. Use a service account as
  owner so schedules survive people moving on.
- A custom interval cannot run more often than the instance's maximum scheduled pipeline
  frequency. Spread schedules out (for example `5 * * * *`, `15 * * * *`) rather than
  stacking them at the top of the hour.
- Scheduled pipelines are subject to the same `workflow:rules`; the usual pattern:
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
nightly-e2e:
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule" && $SCHEDULE_TYPE == "nightly"
build:
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
      when: never              # keep the normal build out of the nightly run
    - when: on_success
```
  Schedule variables (`SCHEDULE_TYPE=nightly`) exist only in that scheduled run. GitLab
  recommends **inputs** (`spec:inputs`, a schedule can have up to 20) for pipeline
  configuration instead of variables.
- **Run** (play button) starts a schedule immediately, at most once per minute, using
  *your* permissions rather than the owner's.
- Audit with `GET /projects/:id/pipeline_schedules` (supports `scope=active|inactive`);
  each schedule carries `cron_timezone`, `active` and `last_pipeline`.
- Schedules stop running when the project or group is marked for deletion.

## 2. Trigger tokens
Settings > CI/CD > Pipeline trigger tokens (Maintainer or Owner to create). The token
impersonates a user's project access and permissions and can start a pipeline for a branch
or tag. A leaked token could force an unscheduled deployment or be used to try to reach CI/CD
variables, so store it in a masked CI/CD variable.
```bash
curl --request POST --fail \
  --form token="$TRIGGER_TOKEN" --form ref=main \
  --form "variables[DEPLOY_ENV]=staging" \
  "https://gitlab.example.com/api/v4/projects/<project_id>/trigger/pipeline"
```
Pipelines started this way have `CI_PIPELINE_SOURCE=trigger` (detect with
`rules: - if: $CI_PIPELINE_SOURCE == "trigger"`) and `CI_PIPELINE_TRIGGERED=true`. Variables
passed in the call have the highest precedence and override same-named variables. Pass
`inputs[name]=value` instead where the pipeline declares `spec:inputs`. Only Owners and
Maintainers can view those variable values on the job page. A revoked token cannot be
re-added. Common errors: 404 can mean a personal access token was used instead of a trigger
token, or a GET instead of POST; 400 means the `ref` does not exist or a rule blocks
`trigger` pipelines.

## 3. Pipelines API
```bash
curl --request POST --fail --header "PRIVATE-TOKEN: $PROJECT_ACCESS_TOKEN" \
  --header 'Content-Type: application/json' \
  --url "https://gitlab.example.com/api/v4/projects/<project_id>/pipeline?ref=main" \
  --data '{"variables":[{"key":"DEPLOY_ENV","value":"staging"},{"key":"CONFIG","value":"...","variable_type":"file"}]}'
```
`ref` is required; `variables` is an array of `key`/`value` (and optional `variable_type`,
`env_var` by default or `file`); `inputs` is a hash. Use a token with API access and set an
expiry.

Poll `GET /projects/:id/pipelines/:pid` and read `status`. The documented status filter
values are `created`, `waiting_for_resource`, `preparing`, `waiting_for_callback`,
`pending`, `running`, `success`, `failed`, `canceling`, `canceled`, `skipped`, `manual`,
`scheduled`. Use a loop with a deadline.

## 4. Webhooks and external systems
Another project's webhook can start a pipeline by calling
`/api/v4/projects/<project_id>/ref/<ref_name>/trigger/pipeline?token=<token>` for push and
tag events; the webhook payload is available to jobs in the file-type variable
`TRIGGER_PAYLOAD`. Do not use pipeline events to trigger pipelines (it returns 403 to avoid
loops). For GitLab to GitLab across projects use the `trigger:` keyword (multi-project
pipelines) or a `CI_JOB_TOKEN`, where `CI_PIPELINE_SOURCE` is `pipeline`.

## 5. Pitfalls
- An empty-pipeline error on a schedule usually means your `workflow:rules` excluded
  `$CI_PIPELINE_SOURCE == "schedule"`.
- A schedule that targets a protected branch needs the owner to hold merge permission on it,
  otherwise protected resources are unavailable and deploys fail.
- The `.gitlab-ci.yml` must have valid syntax before you schedule it; validate it first.

## Verify
- [ ] *Run* on the schedule executes only the intended jobs.
- [ ] Schedule owner is a service account; `GET pipeline_schedules` shows it active.
- [ ] API-started pipelines with variables appear in the pipeline list and honour protected-branch rules.
- [ ] A trigger-token inventory exists and rotation or revocation is planned.

## Checked

2026-10-28. Confirmed against the GitLab docs pages for scheduled pipelines, trigger pipelines with the API, the pipelines API (create a pipeline) and the pipeline schedules API: schedule owner permissions and prerequisites, Inactive state and Take ownership, maximum scheduled pipeline frequency, 20 inputs per schedule, manual Run once per minute using the triggering user's permissions instead of the schedule owner's, trigger token creation roles and path, trigger endpoint and webhook URL, TRIGGER_PAYLOAD, CI_PIPELINE_SOURCE values, variable precedence, 404/400/403 causes, `variables` and `inputs` parameters, pipeline status values, schedule fields. Removed: the 10-schedules-per-project figure, cron jitter and gitlab.com interval claims, `glab` and Terraform commands, the "tokens don't expire / invalid when creator removed" claims, the Restrict pipeline variables setting, the `rules:changes` and `[ci skip]` claims, and the interruptible-schedule claim (none of these were in the fetched pages).

Method: documentation only; no commands were run.
