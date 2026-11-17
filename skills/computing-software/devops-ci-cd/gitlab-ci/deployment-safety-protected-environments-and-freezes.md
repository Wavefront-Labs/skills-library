---
id: computing-software.devops-ci-cd.gitlab-ci.deployment-safety-protected-environments-and-freezes
name: deployment-safety-protected-environments-and-freezes
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, deployment-safety, protected-environments, deployment-tier, freeze-periods, deploy-freeze, ci-deploy-freeze, resource-group, process-mode, oldest-first, newest-first, deployment-approvals, approval-rules, unified-approval, skip-outdated-deployment-jobs, prevent-outdated-deployments, environment-action, stop-environment, on-stop, auto-stop-in, environment-url, deployment-rollback, deploy-keys, group-protected-environments, required-approvals]
level: practitioner
status: docs-checked
description: "Make GitLab deployments safe: protected environments, tiers, approvals, resource_group serialisation, deploy freezes, outdated-deployment prevention and environment stop."
sources: ["https://docs.gitlab.com/ci/environments/deployment_safety/", "https://docs.gitlab.com/ci/environments/protected_environments/", "https://docs.gitlab.com/ci/resource_groups/", "https://docs.gitlab.com/user/project/releases/", "https://docs.gitlab.com/ci/environments/deployment_approvals/", "https://docs.gitlab.com/ci/yaml/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deployment safety: protected environments, resource groups and freezes

**Goal:** only the right people and refs deploy to production, never two deploys at once,
never an older pipeline overwriting a newer one, and nothing ships during a freeze.

## 1. Protected environments
Settings → CI/CD → Protected environments (Maintainer role to protect): **Allowed to deploy**
(roles, users, groups) and **Approvers**. By default any Developer can modify an environment.
- Users in Allowed to deploy need the Developer, Maintainer or Owner role.
- Also protect the **branch** the job runs from: a user with access to the environment but no
  push or merge access to the branch can only deploy. Combine: production environment ← protected
  `main` ← protected variables (protected variables reach only protected branches and tags).
- Group-level protected environments use the **deployment tier** as their name (`production`,
  `staging`, `testing`, `development`, `other`) across projects. Set
  `environment: deployment_tier: production` explicitly in `.gitlab-ci.yml`; an existing environment's
  tier is not updated by adding the keyword later (use the Environments API).

## 2. Deployment approvals (Premium, Ultimate)
With approval rules on a protected environment, every deployment job to it is blocked until the
required approvals are given (Operate → Environments → environment → deployment status badge, or the API).
- The user who triggers the pipeline cannot approve by default; the **Allow pipeline triggerer to approve
  deployment** option changes that. Each user gives one approval per deployment.
- After approval you must still run the job manually; the job need not be `when: manual`.
- Keep required approvals lower than the number of users allowed to deploy.

## 3. resource_group: serialise deploys
```yaml
deploy-prod:
  resource_group: production
  environment: { name: production }
  script: ./deploy.sh
```
Only one job per `resource_group` runs at a time, across pipelines. Default `process_mode` is `unordered`;
change it only through the API to `oldest_first` (oldest pipeline first, safer for continuous
deployment), `newest_first` (newest pipeline first, prevents outdated deployments; jobs must be
idempotent) or `newest_ready_first`.

## 4. Prevent outdated deployments
The **Prevent outdated deployment jobs** setting makes an older deployment job fail ("failed outdated
deployment job") when a newer one has started. Age is the job start time, not the commit time, so
starting an old pipeline's manual job after creating a newer pipeline blocks the newer pipeline's manual
job. **Allow job retries for rollback deployments** is on by default; to roll back, run a new
pipeline on an earlier commit.

## 5. Deploy freezes
Settings → CI/CD → Deploy freezes (Maintainer): `freeze_start` and `freeze_end` are crontab entries
plus a time zone, e.g. `0 18 * * 5` → `0 8 * * 1` (weekend). Overlapping freezes cover the full
overlap. While a job runs inside a freeze, GitLab sets `$CI_DEPLOY_FREEZE`; make your jobs honour it:
```yaml
deploy-prod:
  rules:
    - if: $CI_DEPLOY_FREEZE
      when: manual          # or never
      allow_failure: true
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```
The docs also show a shared `.freezedeployment` job template, extended by deploy jobs, that fails
the job during a freeze so the pipeline can continue without deploying.

## 6. Environment lifecycle
```yaml
deploy-review:
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.example.test
    on_stop: stop-review
    auto_stop_in: 3 days
    deployment_tier: development
stop-review:
  environment: { name: review/$CI_COMMIT_REF_SLUG, action: stop }
  when: manual
  variables: { GIT_STRATEGY: none }    # branch may be deleted by then
  script: ./teardown.sh
```
`on_stop` names the job that closes the environment; `auto_stop_in` stops it after the period and is
reset on each deploy. `action: prepare`, `verify` and `access` do not create deployments (use
`prepare` for smoke tests so they do not pollute deployment history). `environment:kubernetes:`
takes an `agent` and a `dashboard` block for the Kubernetes dashboard (its older `namespace` and
`flux_resource_path` keys are deprecated).

## Verify
- [ ] A developer without deploy rights cannot run the production job.
- [ ] Two pipelines pressing play on prod run one after the other.
- [ ] Playing an older pipeline's deploy after a newer one fails as outdated.
- [ ] During a freeze window the prod job is manual or skipped and `$CI_DEPLOY_FREEZE` is set.

## Checked

2026-10-31. Confirmed against the GitLab deployment safety, protected environments, deployment approvals, resource groups and releases (deploy freeze) pages and the CI YAML reference: default Developer access, Allowed to deploy and Approvers role requirements, group protection by deployment tier, the tier values and deployment_tier behaviour, approval semantics (blocked until approved, triggerer cannot approve by default, one approval per user, manual run after approval, Premium and Ultimate), resource_group process modes and API-only change, outdated-deployment behaviour and rollback retries, freeze cron settings and $CI_DEPLOY_FREEZE, the .freezedeployment template, on_stop, auto_stop_in, environment action values and the kubernetes dashboard keys.
Removed: the "not allowed" error text, the auto-detected tier names, glab and the approval API path, "approval binds to the commit", resource_group cross-project and manual-wait claims, the default-on claim and quoted message for outdated deployments, the Environments rollback button and artifact-expiry advice, the deployments API audit path, the pipeline execution policy claim and the claim that GitLab does not block freeze deployments.

Method: documentation only; no commands were run.
