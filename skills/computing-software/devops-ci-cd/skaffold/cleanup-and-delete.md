---
id: computing-software.devops-ci-cd.skaffold.cleanup-and-delete
name: cleanup-and-delete
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [delete, cleanup, prune, dry-run]
level: intro
status: docs-checked
description: "Remove deployed resources with skaffold delete, automatic cleanup on Ctrl+C and how image pruning works."
sources:
  - "https://skaffold.dev/docs/cleanup/"
  - "https://skaffold.dev/docs/references/cli/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Cleanup removes what Skaffold deployed.

```bash
skaffold delete
skaffold delete --dry-run
```

`--dry-run` prints the resources that would be deleted without deleting them. `delete` also takes `-m/--module`, `-p/--profile`, `-n/--namespace`, `--kube-context`, `--kubeconfig` and `-f/--filename`.

Automatic behaviour:

- `skaffold dev` and `skaffold debug` clean up the deployed resources on `Ctrl+C`, mimicking `skaffold delete`. If Skaffold could not catch the signal, run `skaffold delete` later.
- `--cleanup=false` (dev, debug, run flag, default `true`) turns the resource cleanup off.
- Image pruning removes images built by Skaffold from the local Docker daemon only. It is off by default: it needs artifact caching disabled and `--no-prune=false`, for example `skaffold dev --no-prune=false --cache-artifacts=false`. The CLI describes `--no-prune` as skipping removal of images and containers built by Skaffold during cleanup after dev or debug.
- Images pushed to registries and any application side effects are not cleaned; that is your job.

After `skaffold run` or `skaffold deploy`, running `skaffold delete` removes all the resources you deployed. Use the same profile, namespace and kube-context flags that you deployed with so the right resources are found.

In CI, run `skaffold delete` in a final job for ephemeral environments, with the same `-p` and `-n` as the deploy, and use `--dry-run` first when unsure what will go.

## Checked

2026-11-04. Read the Skaffold Cleanup page and the CLI reference sections for `skaffold delete`, `dev` and `run`. Confirmed: `delete`, `--dry-run`, Ctrl+C cleanup for dev/debug, `--cleanup` default true, image pruning being local-Docker only and needing `--no-prune=false` plus `--cache-artifacts=false`. Removed: the claim that Skaffold uses the `skaffold.dev/run-id` label to find resources to clean (the docs describe that label only for status checking and the resource selector). Conflict: the Skaffold "Dev" workflow page says `--no-prune` disables cleanup of deployed resources on Ctrl+C, but the Cleanup page and CLI reference assign that to `--cleanup` and make `--no-prune` about images; this skill follows the CLI reference. The Cleanup page also says pruning happens on `SIGTERM` in one place and `Ctrl+C` (`SIGINT`) in another.
Method: documentation only; no commands were run.
