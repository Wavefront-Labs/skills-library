---
id: computing-software.devops-ci-cd.semaphore-ui.environment-variable-overrides
name: environment-variable-overrides
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [environment-variables, semaphore-env, configuration, docker, semaphore-ui]
level: practitioner
status: docs-checked
description: "Override any Semaphore option with SEMAPHORE_* variables, including the runner executor JSON variable."
sources:
  - https://semaphoreui.com/docs/admin-guide/configuration/env-vars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure Semaphore with environment variables

Goal: set any option without a config file, typically in containers.

Every option in config.json has an environment variable, and environment variables win over the file. Nested keys use the reference table names, for example `SEMAPHORE_DB_DIALECT`, `SEMAPHORE_TLS_ENABLED`, `SEMAPHORE_HA_REDIS_ADDR`, `SEMAPHORE_METRICS_ENABLED`. Object and list options take JSON strings:

```bash
export SEMAPHORE_OIDC_PROVIDERS='{"github":{"client_id":"***","client_secret":"***"}}'
export SEMAPHORE_FORWARDED_ENV_VARS='["AWS_ACCESS_KEY_ID"]'
```

For runners, the whole executor block can be one variable:

```bash
export SEMAPHORE_RUNNER_EXECUTOR='{"type":"docker","docker":{"image":"semaphoreui/job:latest"}}'
```

This equals `runner.executor.type` plus `runner.executor.docker.*` in the file.

The Semaphore site has interactive generators for Docker server and runner environment blocks, and the reference page lists every option with its variable and default.

Gotchas:
- Quote JSON values so the shell does not split them.
- Some variables are shared between dialects (`SEMAPHORE_DB_HOST` applies to whichever dialect is active).
- Secrets belong in Docker or Kubernetes secrets and `_FILE` variants where offered.

Verify: start the server and confirm the option takes effect (for example the metrics endpoint answers after setting `SEMAPHORE_METRICS_ENABLED=true`).

## Checked

2026-11-04: checked against the environment variables page and the configuration reference. Every claim is stated there.

Method: documentation only; no commands were run.
