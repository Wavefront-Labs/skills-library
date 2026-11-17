---
id: computing-software.devops-ci-cd.turborepo.caching-what-gets-cached-outputs-and-logs
name: caching-what-gets-cached-outputs-and-logs
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, cached-outputs, task-logs, output-logs, outputlogs, log-replay, cache-contents]
level: practitioner
status: docs-checked
description: "Turborepo caches two things per task: files declared in outputs and the terminal logs, replayed on a hit with configurable verbosity."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo caches two types of output: task outputs and logs.

**Task outputs.** The file outputs declared in the `outputs` key of `turbo.json`. On a cache hit, Turborepo restores those files from the cache. The `outputs` key is optional (the configuration reference explains the behaviour when omitted). Warning from the docs: if you do not declare file outputs, Turborepo does not cache them. That may be fine for linters, but many tasks produce files you want cached. If files are unavailable after a cache hit, define the task's outputs.

**Logs.** Turborepo always captures the terminal output of your tasks and restores those logs to your terminal from the first time the task ran. Verbosity of replayed logs is configurable with the `--output-logs` flag of `turbo run` or the `outputLogs` configuration option.

Related caution from the Remote Caching page: logs are treated as artifacts, so be aware of what your tasks print to the console, particularly when sharing a Remote Cache.

Verify: run a task with `--output-logs=errors-only` (see the run reference for values) and confirm replay is quieter.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/caching); commands, flags, key names, defaults and example values were matched against it. Removed: nothing; every claim matched (the remote-caching page confirms logs are treated as artifacts, and the run reference confirms errors-only).

Method: documentation only; no commands were run.
