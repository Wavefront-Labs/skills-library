---
id: computing-software.devops-ci-cd.dagger.cloud-traces-ci-token
name: cloud-traces-ci-token
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, dagger-cloud, traces, observability, ci, github-actions, gitlab-ci, circleci, jenkins]
level: practitioner
status: docs-checked
description: "Connect local runs and CI to Dagger Cloud with dagger login or DAGGER_CLOUD_TOKEN, and manage trace visibility, plus orgs, GitHub App and roles."
sources: [https://docs.dagger.io/0.21/reference/configuration/cloud]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dagger Cloud: connect traces from local and CI

Goal: send traces to Dagger Cloud to visualize and debug runs. Dagger 0.21 docs.

## Account setup

Sign in with GitHub or Google. Organization names: alphanumerics and dashes, unique across Cloud. If you signed up with Google, link GitHub under Settings > Git Sources > Connect GitHub. The Dagger Cloud GitHub App (installed from Git Sources on the org that owns the repos) needs: Commit statuses read/write, Contents read-only, Pull requests read-only.

## Local

```shell
dagger login            # or: dagger login ORGANIZATION-NAME
```

Confirm the code shown in the browser matches the CLI. Alternative: `export DAGGER_CLOUD_TOKEN={your token}`.

## CI

Find the token under the org settings cogwheel > Tokens (or `https://dagger.cloud/{Your Org Name}/settings?tab=Tokens`). Store it as a CI secret and expose it as an environment variable named exactly `DAGGER_CLOUD_TOKEN`:

- GitHub Actions: repository secret, then `DAGGER_CLOUD_TOKEN: ${{ secrets.DAGGER_CLOUD_TOKEN }}` in the Dagger step.
- GitLab CI: project variable, enable Mask and Protect.
- CircleCI: project environment variable; for GitHub, GitLab or Bitbucket add `CIRCLE_PIPELINE_NUMBER: << pipeline.number >>` (GitLab also needs `CIRCLE_PIPELINE_TRIGGER_LOGIN`, `CIRCLE_PIPELINE_REPO_URL`, `CIRCLE_PIPELINE_REPO_FULL_NAME` from `pipeline.trigger_parameters.gitlab.*`).
- Jenkins: Secret text credential with ID `DAGGER_CLOUD_TOKEN`, then `DAGGER_CLOUD_TOKEN = credentials('DAGGER_CLOUD_TOKEN')` in the pipeline environment; use distinct credentials per Cloud org.
- Argo Workflows: `kubectl create secret generic dagger-cloud --from-literal=token=TOKEN`, then expose it as `DAGGER_CLOUD_TOKEN`.

## Visibility and roles

Traces from CI on public repositories are public by default; toggle under org Visibility. Admins can make a single trace public (reversible) or delete one (not recoverable). Roles are `Admin` and `Member`; Admin is not a superset, so give admins who also view runs the Member role too. Roles cannot be changed in the UI; contact support.

## Gotchas

- Regenerating the token breaks every place it is referenced; only do it if leaked.
- Module scanning (Settings > Git Sources > Enable module scanning) finds `dagger.json` files and populates the Modules dashboard.
- Checks and secret providers: computing-software.devops-ci-cd.dagger.cloud-checks-secret-providers.

## Checked

2026-11-07

Read in full from the docs source: reference/configuration/cloud.mdx (Organizations, Traces, Modules, Roles sections). Confirmed the org naming rule, GitHub App permissions, dagger login, token location and URL pattern, per-CI variable setup, public trace behavior, Admin and Member roles, token regeneration warning and module scanning path. No corrections needed.

Method: documentation only; no commands were run.
