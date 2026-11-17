---
id: computing-software.devops-ci-cd.github-actions.serialising-deployments-with-job-level-concurrency
name: serialising-deployments-with-job-level-concurrency
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, deployment-serialisation, job-level-concurrency, deploy-lock, one-deploy-at-a-time, environment-concurrency, terraform-state-lock, cross-workflow-group, queue-deploys, no-cancel-deploy, pending-deploy-superseded, concurrency, deployment-environments]
level: practitioner
status: docs-checked
description: "Serialise deployments per environment with a job-level concurrency group shared across workflows, never cancelling in-flight deploys, and handle the superseded-pending-run case safely."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency", "https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idconcurrency", "https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serialising deployments with job-level concurrency

**Goal:** two merges a minute apart must deploy one after the other, never interleaved, and
never cancel each other halfway through a deploy.

## 1. The pattern
```yaml
jobs:
  build:                     # parallel-safe, no group
    runs-on: ubuntu-latest
    steps: [...]
  deploy-staging:
    needs: build
    environment: staging
    concurrency:
      group: deploy-staging          # literal, shared by EVERY workflow that touches staging
      cancel-in-progress: false      # queue, never kill a running deploy
    runs-on: ubuntu-latest
    steps: [...]
  deploy-prod:
    needs: deploy-staging
    environment: production
    concurrency: { group: deploy-production, cancel-in-progress: false }
    steps: [...]
```
Putting the group on the **job** (not the workflow) lets builds and tests stay parallel while
only the deploy step waits. The group string is repository-wide, so a hotfix workflow using
the same `deploy-production` group queues behind the regular pipeline.

Parametrised form: `group: deploy-${{ inputs.environment || 'staging' }}`.

## 2. What "pending gets cancelled" means for deploys
By default a group allows one running and one pending job or run; a newly queued one replaces the existing
pending one. If three merges arrive, the middle one is cancelled and the newest waits (latest wins).
If every commit must deploy in order (for example sequential database migrations), set `queue: max`
(up to 100 pending, processed first-in-first-out by when each began waiting; cannot be combined with
`cancel-in-progress: true`) or keep a real lock in the deploy tooling.

## 3. Combine with environment protection
`environment:` protection rules (required reviewers, wait timer, deployment branch and tag
restrictions) must pass before a job referencing the environment can proceed. Deployment
branch and tag rules are matched against `GITHUB_REF`. Check how a job waiting on approval
interacts with your concurrency group in a test run before relying on a particular order.

## 4. Gotchas
- A job-level group with `cancel-in-progress: true` will cancel a **running** deploy — only
  acceptable for preview environments.
- Workflow-level and job-level groups both apply; a workflow-level `cancel-in-progress:
  true` for PR CI will still cancel a deploy job inside that workflow. Keep deploys in their
  own workflow or make the workflow-level flag conditional on `pull_request`.
- `concurrency` cannot read `env` or `secrets`; use `inputs`/`vars`/`github`.

## Verify
- [ ] Two overlapping deploy runs: the second shows "Waiting" until the first finishes.
- [ ] A hotfix workflow and the main pipeline never deploy to the same env simultaneously.
- [ ] Superseded pending deploys are an accepted outcome, or `queue: max` is set.

## Checked

Date: 2026-10-25. Documentation release: github/docs main, commit of 2026-10-23.
- Job-level concurrency syntax, allowed contexts (github, inputs, vars, needs, strategy, matrix), one running plus one pending default, replacement of pending, cancel-in-progress, queue single/max with 100 limit, FIFO: confirmed in the concurrency reference text.
- Environment protection rules (required reviewers, wait timer, deployment branches and tags matched against GITHUB_REF): confirmed in the deployments and environments reference.
- Removed the unconfirmed claims about approval versus concurrency ordering, re-run behaviour, and the Terraform, flock and DynamoDB examples.

Method: documentation only; no commands were run.
