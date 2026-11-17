---
id: computing-software.devops-ci-cd.gitlab-ci.pipelines-runners-and-environments
name: pipelines-runners-and-environments
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, gitlab, gitlab-ci-yml, ci-cd, pipeline, stages, jobs, needs, dag, rules, workflow-rules, merge-request-pipelines, duplicate-pipelines, gitlab-runner, cache, artifacts, environments, review-apps, include, extends, id-tokens]
level: practitioner
status: docs-checked
description: "Configure .gitlab-ci.yml well: workflow rules to avoid duplicate MR pipelines, needs-based DAG, cache versus artifacts, interruptible jobs, environments and review apps."
sources: ["https://docs.gitlab.com/ci/yaml/", "https://docs.gitlab.com/runner/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GitLab CI: pipelines, runners and environments

**Goal:** a `.gitlab-ci.yml` that runs once per change (not twice), finishes fast by
running jobs as soon as their inputs are ready, and deploys through tracked environments.

## 1. Stop duplicate pipelines first
Pushing to a branch with an open MR can create both a branch pipeline and an MR pipeline,
usually caused by `rules`. Control it with `workflow:rules`:
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never
    - if: $CI_COMMIT_BRANCH
    - if: $CI_COMMIT_TAG
```
`CI_OPEN_MERGE_REQUESTS` lists up to four MRs using the branch as source and is available in
branch and MR pipelines. The "common if clauses for rules" in the GitLab docs give more patterns.
If a `rules` entry has `when` but no `if`, the lint warns that multiple pipelines may run.

## 2. A baseline pipeline with a DAG
```yaml
stages: [build, test, deploy]
default:
  interruptible: true
  cache:
    key:
      files: [package-lock.json]    # new key when the file content changes
    paths: [.npm/]
    policy: pull                     # most jobs only read the cache

build:
  stage: build
  cache:
    key:
      files: [package-lock.json]
    paths: [.npm/]
    policy: pull-push
  script: [npm ci, npm run build]
  artifacts:
    paths: [dist/]
    expire_in: 1 week

unit:
  stage: test
  needs: [build]                     # starts when build ends, gets its artifacts
  script: [npm test]
  artifacts:
    reports:
      junit: junit.xml

lint:
  stage: test
  needs: []                          # no dependencies: starts immediately
  script: [npm run lint]
```
- `interruptible` marks jobs that may be canceled when a newer pipeline makes them redundant;
  `workflow:auto_cancel:on_new_commit` accepts `conservative` (default), `interruptible` or
  `none`.
- Cache is a speed-up, artifacts are job outputs passed down the pipeline: do not rely on
  the cache for correctness. `cache:key:files` makes the key follow the file contents.
- `needs:artifacts` controls whether a needed job's artifacts are downloaded.

## 3. Rules, not only/except
`rules` is preferred; `only`/`except` are no longer actively developed and should not be
mixed with `rules`. `changes` is always true in some pipeline types (scheduled, tags), so pair
it with an `if` limiting it to branch or MR pipelines.

## 4. Runners
Runners must be registered with GitLab (see the GitLab Runner docs for the current
registration flow for your version). Route jobs with `tags`. Executors and `config.toml`
settings are documented in the Runner docs; check them for your Runner version.

## 5. Variables, secrets and environments
- Protect and mask secret variables. A protected variable reaches only pipelines on protected
  branches or tags, a common cause of an empty variable on feature branches.
- `id_tokens` is a job keyword for OIDC tokens; prefer it to stored cloud keys.
- Review apps: `environment: { name: review/$CI_COMMIT_REF_SLUG, on_stop: stop_review,
  auto_stop_in: 2 days }` plus a stop job. `on_stop` names a different job that closes the
  environment; `auto_stop_in` sets its lifetime. The stop job sets `GIT_STRATEGY: none` in the
  docs' example.

## 6. Reuse and debugging
`include` and `extends` for reuse. Validate in the pipeline editor (Full configuration tab)
or CI Lint; see the debugging skill for details.

## Verify
- [ ] One push to an MR branch produces exactly one pipeline.
- [ ] Jobs with `needs:` start before their stage begins.
- [ ] Review environments auto-stop.

## Checked
2026-10-31. Confirmed on the CI/CD YAML reference and Debugging pages: interruptible and
auto_cancel values, cache:key:files, policy, on_stop, auto_stop_in, GIT_STRATEGY, id_tokens,
duplicate pipeline cause and warning; CI_OPEN_MERGE_REQUESTS on the Predefined variables page.
Removed as unconfirmed: workflow template names, cache per-runner and distributed cache
claims, runner registration commands, executor advice, concurrent setting, resource_group, CI_DEBUG_TRACE,
component syntax, `compare_to` behaviour, node and npm version choices.
Method: documentation only; no commands were run.
