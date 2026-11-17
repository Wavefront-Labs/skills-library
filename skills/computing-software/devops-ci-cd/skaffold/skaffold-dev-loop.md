---
id: computing-software.devops-ci-cd.skaffold.skaffold-dev-loop
name: skaffold-dev-loop
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [dev, watch, inner-loop, trigger]
level: intro
status: docs-checked
description: "Run the continuous development loop: watch files, rebuild, redeploy and clean up on exit."
sources:
  - "https://skaffold.dev/docs/workflows/dev/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`skaffold dev` does a full build, test, render and deploy, then watches your source and repeats whatever is affected.

Action precedence when files change: File Sync, then Build, then Test, then Deploy. Skaffold rebuilds images or syncs files into running containers, then tests and redeploys.

Useful flags:

- `--trigger`: how changes are detected: `notify` (the default, OS filesystem notifications), `polling` (checks on an interval) or `manual` (Skaffold waits for user input).
- `--keep-running-on-failure`: suspend the session on errors in the first build, test, render or deploy rather than exiting; press any key to retry or Ctrl+C to exit.
- `--no-prune`: skip removing images and containers built by Skaffold during cleanup.
- `--cleanup`: defaults to true and deletes the deployments when dev is interrupted.
- `--port-forward`, `--tail` and `--cache-artifacts` adjust forwarding, logs and caching.

On Ctrl+C, Skaffold cleans up the deployed resources so it does not abandon what it created; pass `--cleanup=false` to keep the deployments.

By default Skaffold exits if the first build, test, render or deploy fails. Use `skaffold run` for a single end-to-end pass instead of watching.

## Checked

2026-11-09: confirmed against the Skaffold docs page "skaffold dev" (source docs-v2/content/en/docs/workflows/dev.md) and the CLI reference for dev flags. Corrected the cleanup advice: `--no-prune` skips removing built images and containers, while `--cleanup=false` keeps the deployments. Removed unverified dev-profile advice.

Method: docs-checked 2026-11-09 against skaffold.dev dev workflow page and CLI reference (read as source markdown).
