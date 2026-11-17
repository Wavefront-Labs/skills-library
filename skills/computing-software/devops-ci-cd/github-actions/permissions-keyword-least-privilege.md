---
id: computing-software.devops-ci-cd.github-actions.permissions-keyword-least-privilege
name: permissions-keyword-least-privilege
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, permissions-keyword, job-level-permissions, permissions-scopes, contents-read, pull-requests-write, id-token-write, packages-write, read-all, write-all, permissions-none, least-privilege-permissions, github-token, token-permissions, permission-scope-table]
level: practitioner
status: verified
description: "Set workflow and job permissions to exactly the GITHUB_TOKEN scopes needed: scope table, inheritance, read-all/write-all/{} shortcuts and fixing API 403s."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#permissions", "https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication#permissions-for-the-github_token"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# permissions keyword: least privilege per job

**Goal:** every job's `GITHUB_TOKEN` can do what that job needs and nothing else.

## 1. Syntax and inheritance
```yaml
permissions:            # workflow level: default for all jobs
  contents: read
jobs:
  release:
    permissions:        # job level: this job's token gets exactly the scopes listed here
      contents: write
      packages: write
      id-token: write
  comment:
    permissions:
      pull-requests: write
  docs:
    permissions: {}     # token with no scopes at all (can still read public data)
```
Specifying any scope sets **all unspecified scopes to none** (GitHub docs). Shortcuts: `read-all`,
`write-all`; `permissions: {}` disables all scopes. The token starts from the enterprise, organization or
repository default (permissive or restricted), then the workflow-level and job-level `permissions` keys
adjust it. For a fork `pull_request` (not `pull_request_target`) write scopes are reduced to read unless
the repository enables *Send write tokens to workflows from pull requests*. Under `pull_request_target`
the token has read/write repository permission.

## 2. Scope table (what each unlocks)
| scope | needed for |
|---|---|
| `contents` | read: list commits; write: create a release |
| `pull-requests` | e.g. add a label to a pull request (write) |
| `issues` | e.g. add a comment to an issue (write) |
| `packages` | upload and publish packages on GitHub Packages (write) |
| `id-token: write` | fetch an OpenID Connect (OIDC) token |
| `attestations: write` | generate an artifact attestation for a build |
| `checks` | check runs and check suites (write creates a check run) |
| `statuses` | commit statuses |
| `deployments` | deployments (write creates one) |
| `actions` | e.g. `actions: write` cancels a workflow run |
| `security-events` | code scanning alerts (read lists, write updates status) |
| `pages: write` | request a GitHub Pages build |
| `discussions` | GitHub Discussions |

The workflow syntax reference lists the full current set (newer scopes such as `artifact-metadata` too).
actionlint rejects unknown scopes: `metadata` is not a valid key.

## 3. Diagnosing 403 "Resource not accessible by integration"
1. Which scope does the API call need? (see table / REST docs "Fine-grained access tokens").
2. Does the job's `permissions` block omit the scope? Any scope not listed in a block that lists some is `none`.
3. Is the event a **fork `pull_request`**? Then write scopes are reduced to read unless the repository
   sends write tokens to fork PR workflows.
4. Is it `GITHUB_TOKEN` at all? Events created with it do not start new workflow runs (exceptions:
   `workflow_dispatch` and `repository_dispatch`); use a GitHub App or PAT token to trigger one.

## 4. Practical layouts
- Workflow-level `permissions: { contents: read }` + per-job escalation passes `zizmor` (run with
  `zizmor --offline`: no findings), whereas a job with no `permissions` key at all is reported as
  `excessive-permissions` ("default permissions used due to no permissions: block").
- Reusable workflows: the caller's `permissions` is the ceiling; the called workflow can only keep or
  reduce them, never elevate.

## Verify
- [ ] Every workflow has a top-level `permissions:` block.
- [ ] `zizmor .github/workflows` reports no `excessive-permissions`.
