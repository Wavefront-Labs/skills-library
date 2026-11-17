---
id: computing-software.cloud-infrastructure-engineering.pulumi.github-actions-ci
name: github-actions-ci
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-actions, github-actions, pulumi-ci, pr-preview]
level: practitioner
status: docs-checked
description: "Run Pulumi in GitHub Actions with pulumi/actions v7 (preview, up, comment-on-pr) and OIDC token exchange via pulumi/auth-actions and pulumi/esc-action."
sources:
  - https://www.pulumi.com/docs/iac/guides/continuous-delivery/github-actions/
  - https://github.com/pulumi/actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD with GitHub Actions

```yaml
on:
  pull_request:
    branches: [main]
permissions:
  id-token: write        # OIDC
  pull-requests: write   # comment on PRs
jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pulumi/actions@v7
        with:
          command: preview
          stack-name: org-name/stack-name
          comment-on-pr: true
        env:
          PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
```
`pulumi/actions@v7`: omit `command` to only install the CLI. Inputs: `command` (`up` alias `update`, `refresh`, `destroy`, `preview`, `output`), `stack-name` (fully qualified `org-name/stack-name` outside your personal account; required with a command), `work-dir` (default `./`), `cloud-url` (backend to log in to; needed if no `PULUMI_ACCESS_TOKEN`), `comment-on-pr` (only for `pull_request` events), `comment-on-pr-number`, `github-token` (defaults to `github.token`), `edit-pr-comment` (defaults true since 3.2.0), `refresh` (adds `--refresh` to `preview`/`up`), `diff`, `expect-no-changes`, `secrets-provider`, `config-map`, `policyPacks`, `upsert`, `plan` (save an update plan on preview, read it on up; upload it as an artifact to share between runs), `run-program`.

**Recommended auth: OIDC.** Register GitHub Actions as a trusted OIDC issuer in Pulumi Cloud; `pulumi/auth-actions` exchanges the job's OIDC token for a short-lived Pulumi access token, so no `PULUMI_ACCESS_TOKEN` secret is stored. Pair it with `pulumi/esc-action` to open an ESC environment and inject cloud credentials, secrets and configuration. `pulumi/esc-export-secrets-action` moves existing GitHub secrets into ESC. A job using OIDC needs `id-token: write`, plus `pull-requests: write` if it comments on PRs.

## Gotchas
- v6 changed `refresh`: `up` and `preview` now run with `--refresh` instead of a separate `pulumi refresh` first.
- The action's old env-var inputs were renamed (`PULUMI_ROOT` to `work-dir`, `PULUMI_BACKEND_URL` to `cloud-url`, `COMMENT_ON_PR` to `comment-on-pr`, `GITHUB_TOKEN` to `github-token`).
- `upsert` creates `Pulumi.<stack-name>.yaml`, which must be added back to source control to use that stack further.

## Checked
2026-11-03. Confirmed on the Pulumi GitHub Actions guide and the pulumi/actions README. Fixed: the draft pinned `@v6` as the latest; the README now shows `@v7`. Removed: `aws-actions/configure-aws-credentials` step, Node setup, plugin cache path, fork and `concurrency` advice, and the Verify paragraph.
Method: documentation only; no commands were run.
