---
id: computing-software.devops-ci-cd.earthly.earthly-auto-skip
name: earthly-auto-skip
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, auto-skip, prune-auto-skip, monorepo, static-analysis, run-no-cache, run-push, remote-reference]
level: advanced
status: docs-checked
description: "Use earthly --auto-skip to skip unchanged targets in monorepos: what it needs, which Earthfile features break it, static ARG and IF inference, and clearing the auto-skip cache."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching-in-earthfiles.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/managing-cache.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auto-skip

Goal: skip whole targets when nothing relevant changed, mainly in monorepos.

Auto-skip is a global cache stored in a cloud database (an Earthly Cloud account is required), unlike layer cache and cache mounts which are local to the runner. Enable it for a whole run with `earthly --auto-skip` (caching-in-earthfiles.md says experimental, caching.md says beta); `BUILD --auto-skip` for a single target is "coming soon" on the first page and "experimental" on the second. It is all-or-nothing per target; if not skipped, normal caching applies.

## Static analysis limits
It analyses the build structure up front, so dynamic targets make the build fail with an error message when `--auto-skip` is on.

```
# Supported
ARG MY_ARG=foo
BUILD $MY_ARG

# Not supported
ARG MY_ARG=$(cat ./file)
BUILD $MY_ARG
```
ARG values propagate across targets (`BUILD +target --arg=$MY_ARG`) only when statically known.

`IF`: if the condition can be inferred statically only the taken branch is analysed. Otherwise both `IF` and `ELSE` are analysed and the target is skipped only if both are skipped (supported but inefficient).

Unsupported unless statically inferable (or pinned):
- Dynamic target names (`BUILD $MY_TARGET`, `FROM $MY_TARGET`, `BUILD $(...)`) and dynamic `COPY $MY_FILE .`
- Remote references and remote `IMPORT`s unless pinned to a SHA or a `tags/...` ref: `BUILD github.com/foo/bar:tags/v1.0.0+my-target` works, `github.com/foo/bar:v1.0.0+my-target` does not.
- `GIT CLONE` unless pinned the same way.
- `FOR` loops unless the list is statically inferable.

## Deployments
Auto-skip may also skip `RUN --no-cache` and `RUN --push`. Rollbacks may be skipped unintentionally; remove `--auto-skip`, clear the auto-skip cache, or roll forward with a net-new version.

## Clearing the cache
```bash
earthly prune-auto-skip
earthly prune-auto-skip --path github.com/foo/bar --deep
earthly prune-auto-skip --path github.com/foo/bar --target +my-target
```
The first clears the entire cache for your Earthly org.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: caching/caching-in-earthfiles.md, caching/managing-cache.md, caching/caching.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: replaced the vague maturity wording with what each page says (caching-in-earthfiles.md: experimental and coming soon; caching.md: beta and experimental) and added caching.md to sources.

Method: documentation only; no commands were run.
