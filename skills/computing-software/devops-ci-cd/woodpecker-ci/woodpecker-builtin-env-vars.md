---
id: computing-software.devops-ci-cd.woodpecker-ci.woodpecker-builtin-env-vars
name: woodpecker-builtin-env-vars
category: computing-software
field: devops-ci-cd
product: woodpecker-ci
tags: [environment-variables, ci-variables, built-in]
level: practitioner
status: docs-checked
description: "Look up the built-in CI_ environment variables Woodpecker injects into steps."
sources: ["https://woodpecker-ci.org/docs/usage/environment"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Woodpecker built-in environment variables

Woodpecker injects `CI_*` variables into every step and plugin container. Custom `environment` entries cannot overwrite them.

Each variable has a scope: `config` (available when the YAML is parsed, so usable in `when` filters and string substitution) or `runtime` (only inside the running step, for example step variables and `CI_PIPELINE_STATUS`).

Commonly used:

- Repository: `CI_REPO`, `CI_REPO_OWNER`, `CI_REPO_NAME`, `CI_REPO_URL`, `CI_REPO_CLONE_URL`, `CI_REPO_DEFAULT_BRANCH`.
- Commit: `CI_COMMIT_SHA`, `CI_COMMIT_BRANCH` (target branch for pull requests), `CI_COMMIT_TAG`, `CI_COMMIT_MESSAGE`, `CI_COMMIT_AUTHOR`, `CI_COMMIT_PULL_REQUEST`, `CI_COMMIT_PULL_REQUEST_LABELS`.
- Pipeline: `CI_PIPELINE_NUMBER`, `CI_PIPELINE_EVENT`, `CI_PIPELINE_URL`, `CI_PIPELINE_DEPLOY_TARGET`, `CI_PIPELINE_FILES`.
- Workflow and step: `CI_WORKFLOW_NAME`, `CI_STEP_NAME`, `CI_STEP_TYPE`, `CI_WORKSPACE`.
- Previous run: `CI_PREV_PIPELINE_STATUS`, `CI_PREV_COMMIT_SHA` and related `CI_PREV_*` variables.
- System and forge: `CI_SYSTEM_URL`, `CI_FORGE_TYPE`, `CI_FORGE_URL`, `CI_AGENT_ID`.

`CI_SCRIPT` and the `CI_NETRC_*` variables are internal; do not use them.

`CI_COMMIT_PRERELEASE` is deprecated in favour of `CI_PIPELINE_RELEASE_PRE`. `CI_PIPELINE_FILES` is undefined when more than 500 files changed.

Use them in commands as normal shell variables, in `settings` through `${CI_COMMIT_SHA}` substitution, and in `evaluate` expressions. `CI_PIPELINE_RERUNS` counts restarts and is unset on the first run.

## Checked

2026-11-03. Read the Woodpecker environment page and confirmed the built-in CI_* variable names listed in the skill. Nothing removed. 

Method: documentation only; no commands were run.
