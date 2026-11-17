---
id: computing-software.devops-ci-cd.gitea.actions-variables
name: actions-variables
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-variables, gitea, vars-context, gitea-context, runner-env-vars, event-payload, variable-naming-rules]
level: practitioner
status: docs-checked
description: "Gitea Actions variables: built-in GITEA_/GITHUB_ env vars, gitea.* context, event payload fields, runner env vars, and user-defined vars with naming and precedence rules."
sources: ["https://docs.gitea.com/usage/actions/actions-variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Actions variables and contexts

## Built-in environment variables
Set in every run. `CI`, `GITEA_ACTIONS` and `GITHUB_ACTIONS` are `true` (`GITEA_ACTIONS` lets scripts tell Gitea from other CI). Most variables exist only under a `GITHUB_*` name: `GITHUB_REPOSITORY`, `GITHUB_REPOSITORY_OWNER`, `GITHUB_REF`, `GITHUB_REF_NAME`, `GITHUB_REF_TYPE`, `GITHUB_SHA`, `GITHUB_ACTOR`, `GITHUB_EVENT_NAME`, `GITHUB_EVENT_PATH` (webhook payload file), `GITHUB_SERVER_URL`, `GITHUB_API_URL`, `GITHUB_WORKSPACE`, `GITHUB_RUN_ID`, `GITHUB_RUN_NUMBER`, `GITHUB_RUN_ATTEMPT`, `GITHUB_JOB`, `GITHUB_WORKFLOW`, `GITHUB_BASE_REF`, `GITHUB_HEAD_REF`, `GITHUB_RETENTION_DAYS`. `GITHUB_GRAPHQL_URL` is empty (GraphQL is not supported). Only the file-command paths come under both names: `GITEA_ENV`/`GITHUB_ENV`, `GITEA_OUTPUT`/`GITHUB_OUTPUT`, `GITEA_PATH`/`GITHUB_PATH`, `GITEA_STATE`/`GITHUB_STATE`, `GITEA_STEP_SUMMARY`/`GITHUB_STEP_SUMMARY`. `GITEA_ACTIONS_RUNNER_VERSION` is the runner version. `GITEA_DOCKER_WORKSPACE` is the workspace path as the Docker daemon sees it, for bind mounts into containers a job starts (only set for jobs running in a container), e.g. `${GITEA_DOCKER_WORKSPACE:-.}/data:/app/data`.
Runner variables: `RUNNER_OS`, `RUNNER_ARCH`, `RUNNER_TEMP`, `RUNNER_TOOL_CACHE`. Internal ones such as `ACTIONS_RUNTIME_URL` and `ACTIONS_CACHE_URL` are for actions; the OIDC pair (`ACTIONS_ID_TOKEN_REQUEST_URL`, `ACTIONS_ID_TOKEN_REQUEST_TOKEN`) is only set when configured.

## Context
`${{ gitea.<name> }}` with `github.<name>` as an alias: `gitea.actor`, `gitea.ref`, `gitea.repository`, `gitea.event_name`, `gitea.sha`, `gitea.token`, `gitea.workspace`, `gitea.event`, plus the Gitea-only `gitea.gitea_default_actions_url`.
`gitea.event` is Gitea's webhook payload, close to GitHub's but not identical. A missing field is empty rather than an error. Differences to remember: `create`/`delete` use the full ref (`refs/heads/main`); push has `total_commits` and `compare_url` (GitHub: `compare`); review events use `review.type` (`pull_request_review_approved` etc.) and `review.content`; `issue_comment` uses `is_pull` and has no `event.number` (use `gitea.event.issue.number`). `schedule` runs carry the registering push's payload and `sender.login` is `gitea-actions`.

## User-defined variables
Created at user, organization or repository level; the key is **converted to uppercase**, so write uppercase in YAML. Read with `${{ vars.NAME }}`. Names: letters, digits, underscore; not starting with a digit, `GITHUB_`, `GITEA_` or `CI`; unique per level; case-insensitive. Lowest level wins, so a repository variable beats an organization or user one.

## Checked

2026-11-03: read https://docs.gitea.com/usage/actions/actions-variables/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Rewrote the built-in variable lists: most are `GITHUB_*` only, only the file-command paths have `GITEA_*` twins; removed `ACT`, `RUNNER_NAME`, `RUNNER_WORKSPACE`, `RUNNER_ENVIRONMENT`, `RUNNER_DEBUG`; OIDC pair is set only when configured.
Method: documentation only; no commands were run.
