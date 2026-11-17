---
id: computing-software.devops-ci-cd.github-actions.uses-keyword-forms-local-and-docker-actions
name: uses-keyword-forms-local-and-docker-actions
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, uses-keyword, local-action-uses, docker-uri-uses, uses-ref, uses-subdirectory, private-action-checkout, actions-from-private-repo, docker-hub-action, ghcr-action, uses-sha, uses-branch, uses-tag, action-resolution, workflow-syntax]
level: practitioner
status: verified
description: "Reference actions correctly in uses: owner/repo@ref, owner/repo/path@ref, ./local-path, docker://image:tag; know ref resolution, private-repo access and why local actions need checkout first."
sources: ["https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses", "https://docs.github.com/en/actions/creating-actions/sharing-actions-and-workflows-from-your-private-repository"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# uses: the four reference forms

**Goal:** know exactly what the runner fetches for each `uses:` spelling and when it fails.

## 1. Forms
```yaml
- uses: actions/checkout@v4                           # public repo, tag/branch/SHA
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # SHA (hardened)
- uses: octo-org/tools/.github/actions/lint@main      # action in a subdirectory
- uses: ./.github/actions/build                       # local, relative to repo root
- uses: docker://alpine:3.20                          # image from Docker Hub
- uses: docker://ghcr.io/octo-org/tool:1.2            # image from any registry
```
Always give a remote action a ref (tag, branch or full commit SHA); GitHub recommends a commit SHA as the
safest choice, and the *Require actions to be pinned to a full-length commit SHA* policy rejects
anything else.

## 2. Local actions (`./path`)
- You must check out the repository **before** the step: `./path` is resolved in the runner's workspace.
- Path is relative to `GITHUB_WORKSPACE`, not to the workflow file.
- Inside reusable workflows the "local" path resolves against the workspace (the **caller's** checkout)
  rather than the repository of the running workflow, per GitHub's docs. Use `owner/repo/path@ref`
  to reference an action in the workflow's own repository.

## 3. Private repositories
- Same-org private action: on the action's repo set *Settings → Actions → General → Access* to
  "Accessible from repositories in the '<ORG>' organization"; then `uses: org/private-action@v1`
  works without a token.
- Otherwise check it out with a token: `actions/checkout` with `repository:` and `token:`
  (PAT or GitHub App token with `contents: read`), then `uses: ./path`.

## 4. `docker://`
Runs a Docker image as a container action: the job must run on a Linux runner, `with:` inputs are set as
`INPUT_*` environment variables, and a container action maps `GITHUB_WORKSPACE` to `/github/workspace`.
The image reference forms are `docker://{image}:{tag}` and `docker://{host}/{image}:{tag}`.

## 5. Gotchas
- `uses` and `run` are mutually exclusive in one step (actionlint: `unexpected key "uses" for step to run
  shell command`).
- A `uses:` step does not accept `shell:` or `working-directory:` (actionlint rejects them).
- If an action publishes major version tags (`v4`) they are meant to float forward with each release;
  a SHA never moves.

## Verify
- [ ] Every remote `uses` carries a ref that exists (`git ls-remote https://github.com/o/r v4`).
- [ ] Local actions have a checkout step earlier in the same job.
- [ ] Private actions resolve (no `repository not found` in the "Set up job" log).
