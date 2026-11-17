---
id: computing-software.devops-ci-cd.earthly.earthly-disable-cache-troubleshoot
name: earthly-disable-cache-troubleshoot
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, no-cache, run-no-cache, run-push, cache-troubleshooting, cache-size, save-image, secrets]
level: practitioner
status: docs-checked
description: "Disable Earthly caching with RUN --no-cache, earthly --no-cache or RUN --push, and troubleshoot cache misses from cache size, ARGs and secrets; SAVE IMAGE as manual cache."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching-in-earthfiles.md
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Disable caching and debug cache misses

## Disabling
- One command: `RUN --no-cache echo "Hello"` always executes, even if run before with the same arguments. It does not disable cache mounts or auto-skip, and auto-skip can still skip it.
- Whole run (layer caching and mount caching): `earthly --no-cache +my-target`.
- External effects: `RUN --push` commands are never cached, and run only when Earthly itself is invoked with `earthly --push +my-target`.
- Auto-skip: just remove the `--auto-skip` flag.

## Troubleshooting
**Cache size.** If the configured cache is too small, Earthly garbage-collects layers more often, showing up as random cache misses, usually on the biggest (most expensive) layers. Most common on Mac and Windows where Docker runs in a VM with limited disk. Configure a larger cache for local builds, or launch a larger Satellite for remote builds.

**ARGs.** An ARG declared in a target acts like an environment variable there, so changing it invalidates later `RUN` commands even if unused. Declare ARGs as late as possible, avoid `--global` ARGs, and watch fast-changing ones such as `EARTHLY_GIT_HASH`.

**Secrets.** Secrets do NOT contribute to a layer's cache state; changing a secret does not invalidate the `RUN` that uses it.

**Force a step to stay cached.** If expensive steps keep being evicted even after the above, add `SAVE IMAGE` at strategic points as manual caches, at the cost of simplicity (the page points to the Best Practices section "use SAVE IMAGE to always cache").

## When Earthly is not faster
Per the docs: tight single-language local iteration loops, shared CI environments with languages that cache well, CI where redundant steps are already cached without upload/download, and builds with large files (over 1 GB) due to internal file transfers.

## Gotcha
Unresolved cache problems are to be reported as issues in the Earthly GitHub repository.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: caching/caching-in-earthfiles.md, caching/caching.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
