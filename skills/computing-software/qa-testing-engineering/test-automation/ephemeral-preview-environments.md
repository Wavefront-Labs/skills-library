---
id: computing-software.qa-testing-engineering.test-automation.ephemeral-preview-environments
name: ephemeral-preview-environments
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [ephemeral-environments, preview-environments, ci-integration, kubernetes-namespaces, review-apps]
level: practitioner
status: docs-checked
description: "Give each pull request its own environment for E2E tests: GitLab review apps, Vercel previews, Helm namespace deploys, seeded data and automatic stop."
sources:
  - https://docs.gitlab.com/ci/review_apps/
  - https://vercel.com/docs/deployments/environments
  - https://helm.sh/docs/helm/helm_upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ephemeral test environments per PR

**Goal:** every branch or pull request gets its own running copy of the system, so E2E and exploratory testing happen before merge without fighting over a shared staging.

## Options
- **GitLab review apps**: temporary environments created automatically for each branch or merge request, built on dynamic environments. Define a job with `environment: name: review/$CI_COMMIT_REF_SLUG` and a `url`; you must set up the infrastructure that hosts them. Optional `when: manual` deploys only on demand.
- **Vercel previews**: by default Vercel creates a preview deployment when you push a commit to a non-production branch, open a PR on GitHub, GitLab, Bitbucket or Origin, or deploy with the CLI without `--prod`. Each deployment gets a generated URL; a branch-specific URL tracks the latest on that branch and a commit-specific URL points to that exact deployment. The first deployment of a new project is always a production deployment.
- **Kubernetes namespace per PR** with Helm (below).

## Helm deploy per PR
`helm upgrade` options confirmed on the reference page: `--install` (run an install if the release does not exist), `--create-namespace` (with `--install`), `-n/--namespace`, `--set key=val`, `--wait` and `--timeout` (default 5m0s; time to wait for individual Kubernetes operations).
```
helm upgrade --install app-pr-<PR_NUMBER> ./chart \
  --namespace pr-<PR_NUMBER> --create-namespace \
  --set image.tag=<COMMIT_SHA> --wait --timeout 10m
```
Run your E2E suite against the resulting URL, passing the host in from the pipeline instead of hard-coding it.

## Stopping environments
- GitLab: add `on_stop` to the deploy job and a stop job with `environment: action: stop` to stop the review app when the merge request is merged or the branch is deleted (optionally `when: manual` on the stop job); `auto_stop_in` (for example `1 week`) stops it after a period.
- Anything you create by script (namespaces) needs your own teardown on PR close plus a sweeper for orphans; the cited pages do not provide one.

## Data and secrets
- Seed after deploy (migrations, reference data, test fixtures) so the environment is testable on first load.
- Vercel notes that a staged production deployment uses production environment variables and can reach production services and data; use staging or preview credentials for testing. Every Vercel environment can define its own variables.
- Use non-production credentials in all previews.

## Gotchas
- Cap concurrent previews and stop idle ones to conserve resources (the GitLab docs say stopping conserves resources).
- Shared resources (queues, buckets) need per-PR names to avoid collisions.

## Verify
Opening a PR produces a working URL with seeded data, E2E tests run against it, and closing the PR removes all its resources.

## Checked
2026-11-09: checked against the GitLab "Review apps" page (read in full), the Vercel Environments page (the cited preview-deployments URL redirects there; read in full) and the Helm `helm upgrade` reference (flags install, create-namespace, namespace, set, wait, timeout and its 5m0s default). Removed because the cited pages do not state them: Netlify and Cloudflare Pages, Argo CD ApplicationSet, Okteto, Release and Bunnyshell, the GitHub Actions workflow, `helm uninstall`/`kubectl delete namespace` teardown details, WireMock stubs and `wait-on`. Source URLs updated to the current GitLab and Vercel pages.

Method: documentation only; no commands were run.
