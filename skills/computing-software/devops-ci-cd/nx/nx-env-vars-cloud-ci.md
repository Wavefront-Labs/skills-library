---
id: computing-software.devops-ci-cd.nx.nx-env-vars-cloud-ci
name: nx-env-vars-cloud-ci
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-cloud, environment-variables, ci, ultracache, agents, plugins]
level: practitioner
status: docs-checked
description: "Nx Cloud and CI environment variables: access token, NX_CI_EXECUTION_ID/ENV, NX_BRANCH, timeouts, Ultracache switches, encryption, plus Gradle/Maven/.NET plugin variables."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/environment-variables.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure Nx Cloud and CI behaviour from the pipeline environment.

Auth and identity:
- `NX_CLOUD_ACCESS_TOKEN`: takes precedence over `accessToken` in nx.json (common: read-only token in nx.json, read-write token via env in CI). `NX_CLOUD_AUTH_TOKEN` is deprecated.
- `NX_CLOUD_API`: overrides `nxCloudUrl`.
- `NX_BRANCH`: current branch; must be the PR number for GitHub, Bitbucket and GitLab integrations.
- `NX_CI_EXECUTION_ID`: unique CI run id; the main job and agents must share the value. `NX_CI_EXECUTION_ENV` pairs multiple main jobs (e.g. Linux and Windows) with their agents and selects the matching `overrides` entry in `.nx/ci-config.yaml`. `NX_RUN_GROUP` is the older name.
- `NX_NO_CLOUD=true`: skip Nx Cloud for the run (cannot be used with distributed task execution).

Cache and Ultracache: `NX_CLOUD_USE_ULTRACACHE=false` turns Ultracache off (Nx 24+ uses it in CI by default). `NX_CLOUD_ULTRACACHE_MODE` overrides the workspace setting for one pipeline with `ON`, `WARN`, `ERROR` or `OFF`. `NX_CLOUD_ENCRYPTION_KEY` enables client-side artifact encryption (also `nxCloudEncryptionKey` in nx.json).

Timeouts and retries: `NX_CLOUD_NO_TIMEOUTS` removes the 10 s request timeout; `NX_CLOUD_AGENT_TIMEOUT_MS` and `NX_CLOUD_ORCHESTRATOR_TIMEOUT_MS` default to 3600000; `NX_CLOUD_NUMBER_OF_RETRIES` defaults to 10 on CI, 0 locally; `NX_NO_OUTPUT_TIMEOUT` (e.g. `10m`, `"0"` disables) overrides a launch template.

Agents (bring your own compute only): `NX_AGENT_NAME`, `NX_AGENT_LAUNCH_TEMPLATE`; `NX_WORKING_DIRECTORY` when the workspace is not at the repo root. `NX_CLOUD_DISTRIBUTED_EXECUTION=false` disables DTE (prefer `--no-dte` or `--no-agents`). `NX_CLOUD_DISABLE_METRICS_COLLECTION` stops CPU/memory metrics (collected by default on Nx 22.1+); `NX_SKIP_LOG_GROUPING` stops CI log grouping.

Plugin switches: `NX_GRADLE_DISABLE`, `NX_MAVEN_DISABLE`, `NX_DOTNET_DISABLE` (true when the SDK is absent in CI); graph timeouts `NX_GRADLE_PROJECT_GRAPH_TIMEOUT` and `NX_DOTNET_PROJECT_GRAPH_TIMEOUT` (seconds, default 600 in CI, 120 locally), `NX_MAVEN_ANALYSIS_TIMEOUT`. `NX_DOCKER_IMAGE_REF` (`registry/repository:tag`) overrides the Docker image during a release.

Debugging: for Nx Cloud, `NX_VERBOSE_LOGGING` outputs debug information about agents communicating with the main job, useful for cache misses and on-premises setup issues.

## Checked

2026-11-07. Confirmed: every NX_* variable, default and value listed against the Environment variables page, including the 10 s timeout, 3600000 defaults and plugin graph timeouts. Removed: an invented Verify step; kept the page's NX_VERBOSE_LOGGING statement.

Method: documentation only; no commands were run.
