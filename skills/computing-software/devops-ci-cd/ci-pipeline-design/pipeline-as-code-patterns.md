---
id: computing-software.devops-ci-cd.ci-pipeline-design.pipeline-as-code-patterns
name: pipeline-as-code-patterns
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, pipeline-as-code, ci-yaml, reusable-workflows, workflow-call, composite-actions, gitlab-include, gitlab-ci-components, extends, jenkins-shared-library, jenkinsfile, templates, dry, thin-yaml, ci-scripts, makefile, actionlint, ci-lint, script-injection, pull-request-target, codeowners, pipeline-versioning, github-actions, gitlab-ci, jenkins, buildkite, circleci-orbs]
level: practitioner
status: docs-checked
description: "Structure CI definitions as maintainable code: thin YAML over repo scripts, versioned shared templates, linting and testing pipeline changes, and avoiding injection footguns."
sources: ["https://docs.github.com/en/actions/using-workflows/reusing-workflows", "https://docs.gitlab.com/ee/ci/components/", "https://www.jenkins.io/doc/book/pipeline/shared-libraries/", "https://securitylab.github.com/research/github-actions-untrusted-input/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline-as-code patterns

**Goal:** CI definitions that a new engineer can read in five minutes, change safely,
run locally, and share across fifty repos without copy-paste drift.

(What stages to run and in what order is in
`computing-software.devops-ci-cd.ci-pipeline-design.fast-feedback-pipeline-design`.
This skill is about how the pipeline *code* is organised.)

## 1. Thin YAML, fat scripts
The platform file should say *when* and *where*; scripts in the repo say *what*.
```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<sha>
      - run: make ci-test        # same target a developer runs
```
- Logic in `make`/`just`/`./ci/*.sh`/a task runner is testable, diffable, portable when
  you change CI vendors, and debuggable on a laptop.
- Keep shell scripts strict: `set -euo pipefail`; avoid multi-hundred-line inline
  `run: |` blocks — they hide errors and can't be linted by shellcheck.
- Platform-specific features (caching, artifacts, matrix, OIDC) stay in YAML; that's
  what it's good at.

## 2. Share with versioned templates, not copy-paste
| Platform | Mechanism | Pin by |
|---|---|---|
| GitHub Actions | reusable workflows (`on: workflow_call`), composite actions | tag or commit SHA in `uses: org/ci/.github/workflows/build.yml@v3` |
| GitLab CI | CI/CD components (`include: - component: <fqdn>/<path>/<name>@<version>`) | component version after `@` |
| Jenkins | Shared Libraries (`@Library('ci-lib@v3') _`) with `vars/*.groovy` steps | library version tag |

Rules:
- **Version the shared template like a library** (SemVer tags, changelog). Consumers pin
  a major; a breaking change becomes `v4`, not a surprise on Monday.
- Expose a **small, typed input surface** (`inputs:` with types/defaults). A template
  with 30 boolean flags has become a programming language in YAML; split it.
- Don't over-DRY: three near-identical 10-line jobs are clearer than one job driven by a
  matrix of conditionals. Abstract when the third copy appears *and* they change together.
- Template owners need a test repo that exercises each template on every change.

## 3. Lint and test pipeline changes
- Lint in pre-commit and CI with your platform's own pipeline linter (look up its current command in the platform docs) and run `shellcheck` on scripts.
- Local dry-runs of CI YAML only approximate the hosted runner; don't treat them as proof.

## 4. Security patterns in pipeline code
- **Script injection:** never interpolate untrusted context into `run:` —
  `run: echo "${{ github.event.pull_request.title }}"` executes a crafted title. Pass via
  `env:` and reference `"$TITLE"`.
- `pull_request_target` and `workflow_run` run with secrets on code from forks if you
  check out the PR head. Default to `pull_request`.
- Give `GITHUB_TOKEN` the least privilege each job needs (top-level `permissions:`) and widen per job only where required.
- Pin third-party actions to a full-length commit SHA, and images to digests.
- Protect `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` and the shared-template
  repo with CODEOWNERS review: pipeline code runs with deploy credentials.

## 5. Readability conventions
- One workflow per trigger family (`ci.yml`, `release.yml`, `nightly.yml`), not one
  mega-file with `if:` on every job.
- Name jobs as stable, readable nouns (`lint`, `unit (3.12)`).
- Comment *why* a non-obvious setting exists (`timeout-minutes: 30  # e2e hangs on ...`).
- Set `timeout-minutes` on every GitHub Actions job (the default is 360) and a timeout on other platforms.

## Verify
- [ ] Every CI step can be run locally with one documented command.
- [ ] Shared templates are referenced by version tag/SHA, never a moving branch.
- [ ] A pipeline linter runs on every change to pipeline files.
- [ ] No `${{ ... }}` from event payloads appears directly inside `run:` scripts.
- [ ] Workflow files are CODEOWNERS-protected and default `permissions` are read-only.

## Checked

2026-10-28. Confirmed against the GitHub reusable-workflows page (`on: workflow_call`), GitLab CI/CD components page (`include: - component:` with the version after `@`), Jenkins shared libraries page (`@Library`), GitHub secure-use page (script injection via an intermediate environment variable, `pull_request_target` and `workflow_run` risk with untrusted checkouts, CODEOWNERS for workflow files, pinning actions to a full-length commit SHA, least privilege) and the workflow syntax page (`timeout-minutes`, default 360). Removed: actionlint, GitLab CI Lint API and Jenkins validator commands, `act` and `gitlab-ci-local`, the CircleCI/Buildkite row, Renovate, the path-filter and required-check-rename claims, and GitLab `extends:` / anchors detail.

Method: documentation only; no commands were run.
