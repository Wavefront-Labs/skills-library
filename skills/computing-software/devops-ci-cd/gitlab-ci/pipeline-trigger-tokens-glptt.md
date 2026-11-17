---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-trigger-tokens-glptt
name: pipeline-trigger-tokens-glptt
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, glptt, trigger-token-rotation, trigger-token, pipeline-triggers]
level: practitioner
status: docs-checked
description: "Create and rotate GitLab pipeline trigger tokens, call the trigger API safely, and know which user, variables and inputs the triggered pipeline runs with."
sources: ["https://docs.gitlab.com/ci/triggers/", "https://docs.gitlab.com/api/pipeline_triggers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline trigger tokens (glptt) and rotation

A trigger token impersonates the project access and permissions of the user who created it (Maintainer or
Owner role needed to create one).

## Create and use
```bash
# create
curl -s -X POST -H "PRIVATE-TOKEN: $PAT" -d "description=deploy-from-tooling" \
  "https://gitlab.example.com/api/v4/projects/$PID/triggers"
# trigger
curl -s -X POST --fail \
  -F token="$TRIGGER_TOKEN" -F ref=main \
  -F "variables[DEPLOY_ENV]=staging" \
  "https://gitlab.example.com/api/v4/projects/$PID/trigger/pipeline"
```
In the pipeline: `CI_PIPELINE_SOURCE == "trigger"` (and `CI_PIPELINE_TRIGGERED` is `true`). The docs
use a CI/CD job token to trigger multi-project pipelines and the `trigger:` keyword for downstream
pipelines; both avoid storing a trigger token.

## Rotation
1. Create a new token (description includes date), update the caller's secret store.
2. Confirm calls with the new token (the job page shows part of the token that was used).
3. Delete the old: `DELETE /projects/:id/triggers/:trigger_id` (a revoked token cannot be added back).
List with `GET /projects/:id/triggers` (shows owner and last used).

## Gotchas
- Variables passed as `variables[KEY]=value` have the highest precedence and override same-named
  variables; the docs say `inputs[name]=value` (validated by `spec:inputs`) offers better security.
- Store the token in a masked CI/CD variable and avoid saving it in plain text; the docs show both
  `--form token=` and query-string forms.
- A rule such as `if: $CI_PIPELINE_SOURCE == "trigger"` with `when: never` makes the API return 400;
  a `404` can mean a personal access token or a GET request was used instead of a trigger token POST.

## Verify
- [ ] The new token creates a pipeline and its jobs are labelled as triggered.

## Checked

2026-10-31. Confirmed against the GitLab "Trigger pipelines with the API" page and the pipeline triggers API page: token impersonation and the Maintainer or Owner requirement, curl POST form, CI_PIPELINE_SOURCE trigger and CI_PIPELINE_TRIGGERED, variables[...] precedence, inputs[...] parameter, 400 and 404 troubleshooting causes, job page token display, revoked tokens cannot be restored, and the GET and DELETE trigger endpoints with owner and last_used fields.
Removed: the `glptt-` prefix (not stated in either page), blocked-user token behaviour, the minimum-role variable setting claim, the ref-limiting claim and the log-leak claim.

Method: documentation only; no commands were run.
