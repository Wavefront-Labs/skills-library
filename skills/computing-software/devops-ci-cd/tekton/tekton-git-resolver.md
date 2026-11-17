---
id: computing-software.devops-ci-cd.tekton.tekton-git-resolver
name: tekton-git-resolver
category: computing-software
field: devops-ci-cd
product: tekton
tags: [resolvers, git-resolver, remote-resolution, caching]
level: practitioner
status: docs-checked
description: "Fetch Tekton Tasks and Pipelines from a Git repository with the git resolver, including anonymous clone versus authenticated SCM API, tokens, revisions and caching."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/git-resolver.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resolver type `git`. Parameters: `url` (anonymous clone) or `repo` plus `org` (authenticated API) but not both; `revision` (SHA-1/SHA-256 commit, branch or tag); `pathInRepo` (for example `task/golang-build/0.3/golang-build.yaml`); `token`/`tokenKey` (secret in the PipelineRun namespace for the API); `gitToken`/`gitTokenKey` (for `git clone`; empty means anonymous); `serverURL`; `scmType` (`github`, `gitlab`, `gitea`); `cache`.

Requirements: Tekton Pipeline v0.41.0 or later, built-in resolvers installed, `enable-git-resolver: "true"` in the `resolvers-feature-flags` ConfigMap in namespace `tekton-pipelines-resolvers`, and beta features enabled.

Operator config (its ConfigMap): `default-revision`, `default-url`, `default-org`, `scm-type`, `server-url`, `api-token-secret-name`/`-key`/`-namespace`, `fetch-timeout` (a global maximum of 1 minute is enforced on all resolution requests), and backoff settings `backoff-duration` (2s), `backoff-factor` (2.0), `backoff-jitter` (0.1), `backoff-steps` (2; set 1 to disable retries) and `backoff-cap` (10s).

Caching via the `cache` param: `always`, `never`, or `auto` (default; only caches when the revision is a commit hash, since branches and tags move). The `cache` param must sit under `pipelineRef.params` or `taskRef.params`, not `spec.params`.

## Checked

Checked 2026-11-08 against docs/git-resolver.md in tektoncd/pipeline (main), read in full. Confirmed parameters, the url versus repo plus org rule, requirements, operator options, one-minute global timeout, backoff defaults, cache modes and the cache param placement. No changes needed to claims.

Method: documentation only; no commands were run.
