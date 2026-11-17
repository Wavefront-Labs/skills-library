---
id: computing-software.devops-ci-cd.atlantis.atlantis-pre-and-post-workflow-hooks
name: atlantis-pre-and-post-workflow-hooks
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [pre-workflow-hooks, post-workflow-hooks, dynamic-config, infracost, untrusted-input]
level: advanced
status: docs-checked
description: "Use pre and post workflow hooks to generate atlantis.yaml or report after runs, and keep PR-derived variables safe."
sources: ["https://www.runatlantis.io/docs/pre-workflow-hooks", "https://www.runatlantis.io/docs/post-workflow-hooks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis pre and post workflow hooks

Hooks run scripts before (`pre_workflow_hooks`) or after (`post_workflow_hooks`) the default or custom workflow. Unlike custom workflow steps they do not need the repo config to exist, and their output is not posted back to the PR. Define them only in server-side repo config under `repos`.

Keys: `run`, `description`, `shell` (default `sh`), `shellArgs` (default `-c`). The `commands` key restricts a hook to a comma-delimited list such as `plan, apply`; otherwise it runs for every command.

By default a failing pre hook does not stop plan or apply; the `fail-on-pre-workflow-hook-error` server flag changes that.

Use cases: generate `atlantis.yaml` right before Atlantis parses it (for example with `terragrunt-atlantis-config generate` using `shell: bash`, `shellArgs: -cv`), or after plans run `infracost output` to merge per-project JSON into a Markdown cost report.

Environment: `BASE_REPO_NAME`, `BASE_REPO_OWNER`, `HEAD_REPO_NAME`, `HEAD_REPO_OWNER`, `HEAD_BRANCH_NAME`, `HEAD_COMMIT`, `BASE_BRANCH_NAME`, `PULL_NUM`, `PULL_URL`, `PULL_AUTHOR`, `DIR`, `USER_NAME`, `COMMENT_ARGS`, `COMMAND_NAME`, `OUTPUT_STATUS_FILE` (write `failure` to mark the hook failed), `PROJECT_NAME`. Post hooks also get `COMMAND_HAS_ERRORS`.

Security: branch names, authors and comment args come from the PR and are untrusted. Atlantis passes them as environment variables, never interpolated into the command, so plain `$HEAD_BRANCH_NAME` is safe. The protection is lost if you re-evaluate the value with `eval`, a nested `sh -c`, or write it into a script you then execute.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Pre Workflow Hooks, Post Workflow Hooks. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
