---
id: computing-software.devops-ci-cd.github-actions.workflows-runners-and-caching
name: workflows-runners-and-caching
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, github, ci, cd, ci-cd, workflow, yaml, runners, self-hosted-runner, matrix, matrix-build, cache, actions-cache, setup-node, setup-python, concurrency, reusable-workflows, workflow-call, oidc, permissions, github-token, pull-request-target, release-automation, artifacts, pinning-actions]
level: practitioner
status: docs-checked
description: "Write fast, safe GitHub Actions workflows: triggers, least-privilege token, matrix builds, dependency caching, concurrency, reusable workflows and OIDC deploys."
sources: ["https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax", "https://docs.github.com/en/actions/reference/security/secure-use", "https://github.com/actions/setup-node#readme"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitHub Actions — workflows, runners and caching

**Goal:** a workflow in `.github/workflows/*.yml` that gives feedback in minutes, never
leaks a secret to a fork, and is easy to reuse across repos.

## 1. A solid baseline workflow
```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read            # default the GITHUB_TOKEN to read-only
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 20      # default is 360
    strategy:
      fail-fast: false
      matrix:
        node: [20, 22]
        os: [ubuntu-latest]
        include:
          - node: 22
            os: windows-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node }}
          cache: npm           # built-in dependency caching
      - run: npm ci
      - run: npm test
```
Key choices: `permissions` at the top (then widen per job, e.g. `contents: write`
only on the release job); `concurrency` cancels superseded PR runs but not `main`
runs; `fail-fast: false` so one red matrix cell doesn't hide the others.

## 2. Caching that actually hits
- Prefer the built-in caching of the setup actions: `setup-node` (`cache` input; since v6 npm caching is automatic
  when `package.json` sets `packageManager` or `devEngines.packageManager` to npm), `setup-python` (`cache: pip`,
  off by default; pipenv and poetry also supported), `setup-go` (`cache` defaults to true) and `setup-java`
  (`cache: maven|gradle|sbt`).
- For anything else, `actions/cache` (README examples use `@v6`) with a key that changes only when inputs do:
  `key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}` plus
  `restore-keys: ${{ runner.os }}-cargo-` for a partial hit.
- **Gotcha, scoping:** caches are scoped to key, version and branch; the default branch cache is available to
  other branches. Warm the cache with a run on the default branch.
- **Gotcha, keys:** include a lockfile hash in the key so it changes with the inputs.
- Repository cache storage is limited (10 GB by default; entries unused for over 7 days are removed and the
  oldest-accessed entries are evicted first when the limit is reached).

## 3. Reuse: composite actions vs reusable workflows
- **Reusable workflow** (`on: workflow_call` with `inputs:`/`secrets:`) — whole jobs,
  own runners; call with `jobs.x.uses: org/repo/.github/workflows/build.yml@v1`.
  The caller must pass secrets by name or write `secrets: inherit`.
- **Composite action** (`action.yml` with `runs.using: composite`) — a bundle of steps
  that runs inside the caller's job. Each `run` step in a composite action must specify `shell`.

## 4. Security gotchas (the ones that cause incidents)
- **Pin third-party actions to a full commit SHA**, not a tag
  (a full-length commit SHA is documented as the way to pin an action to an immutable release). Pin to a tag
  only if you trust the creator.
- **Never** check out and run PR code under `pull_request_target`: it runs with the base repository's
  secrets and a read/write token. Use plain `pull_request` for untrusted code.
- **Script injection:** don't interpolate `${{ github.event.pull_request.title }}`
  (or issue bodies, branch names) directly into `run:`. Pass via `env:` and quote
  `"$TITLE"` in the shell.
- **Cloud deploys via OIDC** instead of long-lived keys: add `permissions: id-token: write`
  and configure the cloud provider's trust policy on the token's claims (see the OIDC documentation for the
  `sub` claim formats).
- Put production deploys behind an **environment** with required reviewers; environment
  secrets are only released to jobs that name that `environment:`.

## 5. Runners
- GitHub-hosted runners execute in ephemeral, clean isolated virtual machines; the `-latest` labels may not be the
  newest OS, so pin a version label when you depend on a toolchain.
- Self-hosted runners are not guaranteed to be ephemeral or clean and can be persistently compromised by
  untrusted workflow code, so GitHub advises against using them with public repositories. Prefer just-in-time
  (ephemeral) runners created through the REST API, and target runners by labels:
  `runs-on: [self-hosted, linux, gpu]`.

## 6. Debugging
- Re-run with debug logging enabled, or set the repository secret or variable `ACTIONS_STEP_DEBUG` to `true`
  (and `ACTIONS_RUNNER_DEBUG` for runner diagnostic logs).
- Use `if: failure()` or `if: always()` steps for uploading logs with `actions/upload-artifact`.

## Verify
- [ ] Workflow-level `permissions:` is set; only release/deploy jobs widen it.
- [ ] Second run on the same lockfile shows "Cache restored from key" in setup logs.
- [ ] A new push to a PR cancels the previous run of that PR.
- [ ] Third-party actions are SHA-pinned.
- [ ] No `pull_request_target` job checks out the PR head; no `${{ }}` of user text inside `run:`.
- [ ] Every job has `timeout-minutes`.

## Checked

Date: 2026-10-25. Documentation release: github/docs commit of 2026-10-23 and setup-* and actions/cache READMEs.
- timeout-minutes default 360, concurrency and permissions syntax, composite and reusable workflow rules: confirmed in workflow-syntax, metadata-syntax and reuse-workflows.
- Setup-action caching (setup-node v6 automatic npm caching, setup-python cache off by default with pip/pipenv/poetry, setup-go cache default true, setup-java maven/gradle/sbt) and current majors: confirmed in the setup-* READMEs; cache scope and limits: confirmed in actions/cache README and the dependency-caching reference.
- SHA pinning, pull_request_target risk, runner ephemerality and JIT runners, debug secrets: confirmed in secure-use, the pull_request_target text and enable-debug-logging.
- Removed unconfirmed claims: Dependabot ecosystem key, act, actionlint, cloud login action names, trust-policy string, the SHA-pin example with a version comment.

Method: documentation only; no commands were run.
