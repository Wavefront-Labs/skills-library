---
id: computing-software.devops-ci-cd.gitlab-runner.runner-custom-executor
name: runner-custom-executor
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [custom-executor, config-exec, prepare-exec, run-exec, cleanup-exec]
level: advanced
status: docs-checked
description: "Drive a bespoke environment with the Custom executor's stage executables."
sources: ["https://docs.gitlab.com/runner/executors/custom/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Custom executor

The custom executor delegates job stages to executables configured in `[runners.custom]`. Stages run in order: `config_exec`, `prepare_exec`, `run_exec`, `cleanup_exec`.

Each stage has its own executable and arguments, and config, prepare and cleanup have timeouts (`config_exec_timeout`, `prepare_exec_timeout`, `cleanup_exec_timeout`; default 3600 seconds). `graceful_kill_timeout` and `force_kill_timeout` (default 600 seconds each) bound termination.

The runner provides `BUILD_FAILURE_EXIT_CODE`; your executable should exit with that code to mark a job failure in GitLab CI. If the user's script in `.gitlab-ci.yml` exits non-zero, `run_exec` should exit with `BUILD_FAILURE_EXIT_CODE`.

Services are exposed as a JSON array in `CUSTOM_ENV_CI_JOB_SERVICES`.

The custom executor is in maintenance mode.

## Checked

2026-11-03. Confirmed against stages, timeouts and defaults on Custom executor and Advanced configuration, BUILD_FAILURE_EXIT_CODE, CUSTOM_ENV_CI_JOB_SERVICES and maintenance mode. Replaced the unsourced `*_args` wording.

Method: documentation only; no commands were run.
