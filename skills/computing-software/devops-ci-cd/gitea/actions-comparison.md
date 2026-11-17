---
id: computing-software.devops-ci-cd.gitea.actions-comparison
name: actions-comparison
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-actions-vs-github, gitea, builtin-checkout, self-prefix, workflow-relative-actions, unsupported-syntax, default-actions-url]
level: practitioner
status: docs-checked
description: "Know where Gitea Actions differs from GitHub Actions: uses prefixes self, builtin and $/, extra cron macros, ignored environment key, runs-on forms, package auth gap."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/actions/comparison.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea Actions versus GitHub Actions

Designed to be compatible, with these differences.

## Extras
- `uses:` takes an absolute URL, e.g. `uses: https://gitea.com/actions/checkout@v4`.
- Prefixes: `self:` for your own instance (`uses: self:owner/repo@v1`, or `self:owner/repo/.gitea/workflows/build.yml@v1`) and `builtin:` for actions inside Gitea Runner, with no download and no Node in the image (`uses: builtin:checkout`). `builtin:checkout` accepts only `repository`, `ref`, `token`, `path` and `fetch-depth`, with `actions/checkout` defaults, and **fails on any other input**.
- `$/` refers to the repository and commit of the workflow (or enclosing composite action), e.g. `uses: $/.gitea/actions/build`, and unlike `./` needs no checkout first.
- `schedule` also accepts `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly`.
- Actions can be written in Go.

## Unsupported
- `jobs.<job_id>.environment` is ignored.
- `runs-on` supports static strings (`self-hosted`), label arrays (`[linux, self-hosted]`), string expressions and arrays containing expressions, e.g. `${{ github.event_name == 'push' && 'ubuntu-latest' || 'self-hosted' }}`; nothing more complex.
- Problem matchers and error annotations are ignored.
- Pre/post steps and service steps have no log section of their own.
- Context availability is not checked, so contexts like `env` work in more places.

## Different behaviour
- `GITEA_TOKEN` cannot publish to its repository's package registry (for example pushing OCI images); use a personal access token.
- `permissions` shapes `GITEA_TOKEN` and is clamped (see `gitea-actions-token-permissions`).
- A bare `uses: actions/checkout@v4` downloads from `https://github.com`, or from your instance when `[actions].DEFAULT_ACTIONS_URL` is `self`.

## Checked
2026-11-03. Every claim confirmed against the Gitea docs page comparison.md (raw markdown, gitea/docs main branch). Nothing removed.
Method: documentation only; no commands were run.
