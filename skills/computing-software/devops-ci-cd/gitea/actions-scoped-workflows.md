---
id: computing-software.devops-ci-cd.gitea.actions-scoped-workflows
name: actions-scoped-workflows
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-scoped-workflows, gitea, scoped-workflow-dirs, required-workflows, workflow-source-repository, merge-gate-status-checks]
level: advanced
status: docs-checked
description: "Run centrally maintained Gitea workflows on many repositories with scoped workflows: source repos, owner or instance level, SCOPED_WORKFLOW_DIRS, required checks and limits."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/actions/scoped-workflows.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea scoped workflows

Keep workflows in one **source** repository and run them on many **consuming** repositories. The run happens in the consumer's context (its runners, secrets, `GITEA_TOKEN`, branch) while the YAML is read from the source, pinned to the source's default-branch commit at event time.

## Levels
- Owner level: registered by an organization or user; applies to repositories they own.
- Instance level: registered by an administrator; applies to every repository and a required one cannot be opted out. Register deliberately.
A repository registered at both levels is still evaluated once per event.

## Configuration
```ini
[actions]
SCOPED_WORKFLOW_DIRS = .gitea/scoped_workflows
```
Default as shown; comma-separated list allowed; **must not overlap** `WORKFLOW_DIRS` (default `.gitea/workflows` and `.github/workflows`). Empty means none are found or run, though sources can still be registered. Only files in this directory count, so the source's own regular Actions are unaffected.

## Providing and registering
1. Commit workflows (e.g. `.gitea/scoped_workflows/lint.yaml`) on the source's **default branch**.
2. Register under Organization Settings, Actions, Scoped Workflows; User Settings, Actions, Scoped Workflows; or Site Administration, Actions, Scoped Workflows.
The `on:` triggers must match the consumer's event. Consumers can disable a workflow from their Actions page unless it is required.

## Required workflows
Mark a workflow **required** and give it status-check glob patterns (one per line). It cannot be disabled, and a consuming pull request merges only when a commit status matching **every** pattern passed; a check that never posts blocks the merge. The context format is `<source repo full name>: <workflow display name> / <job> (<event>)`, e.g. pattern `my-org/ci-repo: Lint / *`. Enforced on target branches that have a branch protection rule (even with its own status checks off), not on unprotected branches.
**Trap**: only events that post commit statuses (`push`, `pull_request`, `pull_request_target`, `release`) can be required. A workflow limited to `workflow_dispatch`, `schedule` or `workflow_call` posts no status and would block every pull request forever.

## Reusable workflows
Local `uses: ./...` or `uses: $/...` resolve against the source repository. Cross-repository `owner/repo/...@ref` or `self:owner/repo/...@ref` resolve with the consumer's read permission, so private targets must be readable by every consumer.

## Limits
`on: schedule` and `on: workflow_run` are not supported as scoped triggers; only the source's default branch is used. Logs of the source's steps are readable by anyone who can view the consumer's Actions, so a private source leaks its logic.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page scoped-workflows.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
