---
id: computing-software.devops-ci-cd.gitlab-ci.rules-variables-overrides
name: rules-variables-overrides
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, rules-variables, conditional-variables, per-branch-variables]
level: practitioner
status: docs-checked
description: "Set job variables conditionally with rules:variables so one job definition deploys differently per branch, tag or pipeline source, without duplicating jobs."
sources: ["https://docs.gitlab.com/ci/yaml/#rulesvariables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rules:variables

## 1. One job, many configurations
```yaml
deploy:
  variables:
    DEPLOY_ENV: dev
    REPLICAS: "1"
  rules:
    - if: $CI_COMMIT_TAG
      variables: { DEPLOY_ENV: production, REPLICAS: "6" }
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      variables: { DEPLOY_ENV: staging, REPLICAS: "2" }
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  environment: { name: $DEPLOY_ENV }
  script: ./deploy.sh "$DEPLOY_ENV" "$REPLICAS"
```
The first matching rule wins; its `variables` override the job's `variables`.

## 2. Precedence reminders
rules:variables beat job `variables` and global `variables`, but **lose** to project/group
CI/CD settings variables, pipeline/trigger/schedule variables and manual-run variables. If a
project variable `DEPLOY_ENV` exists, your rule does nothing.

## 3. Uses
- Feed values such as the deploy target to the job's script.
- Toggle tool flags: `{ PYTEST_ADDOPTS: "-m 'not slow'" }` on MRs, full suite on main.
- Pair with `workflow:rules:variables` for pipeline-wide values (applies to all jobs).

## 4. Gotchas
- The variables only exist if that rule matched — a later `- when: on_success` catch-all gets job defaults.
- Values are strings; quote numbers/booleans (`"6"`, `"true"`).
- Rules are evaluated at pipeline creation: a variable set in rules cannot be based on job output
  (use dotenv artifacts for that).

## Verify
- [ ] Tag pipeline's deploy job shows `production` in the environment column; MR job shows `dev`.

## Checked

2026-11-02. Confirmed: `rules:variables` and `workflow:rules:variables` exist, workflow variables become defaults for all jobs; precedence order puts manual job variables, pipeline variables and project/group/instance variables above variables defined in the YAML (GitLab CI/CD YAML reference and variables docs). Removed: environment:name/resource_group expansion claim and the same-rule reference claim.

Method: documentation only; no commands were run.
