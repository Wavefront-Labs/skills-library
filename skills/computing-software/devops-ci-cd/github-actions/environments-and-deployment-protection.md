---
id: computing-software.devops-ci-cd.github-actions.environments-and-deployment-protection
name: environments-and-deployment-protection
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, deployment-environments, deployment-protection-rules, environment-protection, required-reviewers, wait-timer, environment-branches, deployment-branch-policy, environment-secrets, environment-variables, deployments-api, deployment-status, custom-protection-rules, github-app-gate, prevent-self-review, environment-url, deployment-history, active-deployments, production-gate, approval-gate]
level: practitioner
status: docs-checked
description: "Gate GitHub Actions deploys with environments: required reviewers, wait timers, branch/tag policies, env-scoped secrets, custom protection rules and deployments API records."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments", "https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments", "https://docs.github.com/en/actions/reference/limits"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Environments and deployment protection

**Goal:** production deploys need an approval, can only come from `main` or release tags,
use secrets that no PR workflow can read, and leave an auditable deployment record.

## 1. Declare the environment on the job
```yaml
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: ${{ steps.deploy.outputs.url }}   # shows as "View deployment" on the run and PR
    concurrency: production                  # concurrency group; see the concurrency skills
    steps:
      - id: deploy
        run: ./deploy.sh && echo "url=https://app.example.test" >> "$GITHUB_OUTPUT"
```
Running a workflow that references a nonexistent environment creates it, normally without protection rules, so
configure it under *Settings, Environments* (or the REST API) before first use. Environments are available for
public repositories on Free, Pro and Team plans; on those plans private repositories cannot configure them.

## 2. Protection rules (Settings, Environments)
- **Required reviewers**: up to 6 users or teams; only one needs to approve. *Prevent self-review* stops the person
  who started the deployment from approving it.
- **Wait timer**: an integer from 1 to 43,200 minutes (30 days); wait time is not billed.
- **Deployment branches and tags**: *No restriction*, *Protected branches only*, or *Selected branches and tags*
  with name patterns matched against the run's `GITHUB_REF` (wildcards do not match `/`; use `release/*/*` for
  an extra slash). Add `refs/pull/*/merge` only if `pull_request` runs should deploy.
- **Allow administrators to bypass configured protection rules**: deselect it to disallow bypass.
- **Custom protection rules** powered by GitHub Apps: any number of apps can be installed, but at most 6 rules
  can be enabled on one environment.
- A workflow may wait up to 30 days for environment approval.

## 3. Environment-scoped secrets and variables
Environment secrets are only available to jobs that use the environment, and only after configured rules (for
example required reviewers) pass. An environment secret with the same name as a repository or organisation secret
takes precedence for the job that sets `environment`. Environment variables (`vars`) are scoped the same way.
For reusable workflows, the caller must still pass secrets (`secrets: inherit` or by name).

## 4. Deployment history
Jobs that reference an environment create deployments that appear in the repository's deployment history. For the
deployment objects, statuses and REST endpoints, use the deployments documentation.

## 5. Patterns
- **Staging then production**: two jobs, `needs: deploy-staging`, the second with `environment: production`.
- **Manual-only prod**: `workflow_dispatch` plus a selected-branches policy that allows only `main`.
- Split long jobs so the approval gate sits right before the irreversible action.

## 6. Gotchas
- Deleting an environment deletes its secrets and protection rules, and jobs waiting on its rules fail.
- Converting a repository from public to private on a Free, Pro or Team plan makes configured rules and secrets
  ignored.

## Verify
- [ ] Running the prod job from a non-allowed branch is blocked by the branch policy.
- [ ] The run page shows the approval and the deployment appears in the deployment history.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Required reviewers (up to 6, one approves), self-review prevention, wait timer 1-43,200 minutes, deployment branch and tag options and GITHUB_REF matching, administrator bypass, 6-rule maximum for custom rules: confirmed in the deployments-and-environments reference and manage-environments page. The skill's earlier wait-timer range starting at 0 was wrong.
- Environment secret scoping and precedence, implicit environment creation, deletion effects, plan restrictions: confirmed in manage-environments and the reusable-workflow secrets text; 30-day approval wait: confirmed in the limits reference.
- Removed unconfirmed deployments-API details, error-message text, audit-log event names, matrix approval behaviour, third-party action examples and the evaluation-order claim.

Method: documentation only; no commands were run.
