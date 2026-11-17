---
id: computing-software.devops-ci-cd.earthly.earthly-practice-secrets-push-and-ci
name: earthly-practice-secrets-push-and-ci
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, best-practices, secret, run-push, ci, strict, locally, remote-cache]
level: practitioner
status: docs-checked
description: "Safe secret handling with RUN --secret and secret mounts, RUN --push for deploys, --ci in CI, avoiding LOCALLY, pushing on main only, and not wrapping earthly in scripts."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Practices: secrets, push and CI

## Secrets
Pass secrets with `earthly --secret`, Earthly Cloud Secrets and `RUN --secret`, never `ARG` (leaks into logs, cache and possibly images). Do not write secrets into files that stay in a layer. Best way for secret files:
```Dockerfile
RUN --mount=type=secret,target=/root/.aws/credentials,id=AWS_CREDENTIALS \
    aws ec2 describe-images
```
If you must write a file, remove it in the same `RUN`; deleting it in a later `RUN` leaks it to the cache.

## Deployments
Use `RUN --push --secret GITHUB_TOKEN github-release upload ...` rather than `RUN --no-cache`. `--push` runs only in push mode (`earthly --push`), never reuses cache, and runs in the push phase after testing succeeded. `RUN --no-cache` may run in parallel with tests and even without `--push`.

## CI
`--ci` expands to `--no-output --use-inline-cache --save-inline-cache --strict`: no non-repeatable commands, inline cache on, no output on the CI host. In `--strict` or `--ci`, `LOCALLY` is not allowed. Valid `LOCALLY` uses: installing host dependencies for IDEs, running tests on the host docker daemon for debugging, and dev commands that would need copying very large files.

Push on `main` only to balance cache freshness against upload time:
- main: `earthly --ci --push +target`
- PR: `earthly --ci +target`
`EARTHLY_PUSH` sets push via env var. A more extreme variant is `earthly --ci --push --remote-cache=.... --max-remote-cache +target`; measure per project.

## Debug
`earthly -i +my-target` drops into the failed container; press `Ctrl+D` to exit.

## Do not wrap earthly
Antipatterns: calling earthly repeatedly in a script, computing ARGs outside, a bash `for` loop over targets, building once without and once with `--push`, repeated `--no-cache` runs to order a deploy. Use an `all` target and one invocation.

## Gotchas
- Private code can leak through cache image tags; use private repositories for closed-source projects.
- `RUN --ssh go mod download` passes host SSH agent access.

## Checked

2026-11-07. Read docs/guides/best-practices.md in full. The secrets, RUN --push, --ci, LOCALLY, remote-cache, interactive and anti-pattern sections all match. Nothing removed.
Method: documentation only; no commands were run.
