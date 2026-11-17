---
id: computing-software.devops-ci-cd.argocd-image-updater.run-interval-concurrency-and-leader-election
name: run-interval-concurrency-and-leader-election
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, interval, max-concurrent-apps, max-concurrent-reconciles, leader-election, run-flags, polling]
level: practitioner
status: docs-checked
description: "Tune the run command: --interval and its precedence, concurrency limits for apps and CRs, and leader election with its RBAC trap."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run flags: interval, concurrency, leader election

Polling interval: `--interval <duration>` (default `2m0s`). Durations need a unit (`2m`, `30s`); with no unit milliseconds are assumed. `0` reconciles once and stops for that ImageUpdater CR. Precedence: the `--interval` flag, then env `IMAGE_UPDATER_INTERVAL`, then the default.

Concurrency:

- `--max-concurrent-apps <n>` (env `MAX_CONCURRENT_APPS`): applications processed in parallel; `1` disables concurrency.
- `--max-concurrent-reconciles <n>` (env `MAX_CONCURRENT_RECONCILES`): ImageUpdater CRs reconciled simultaneously; `1` disables it. Higher values may improve throughput but raise resource use and API load.
- The `webhook` command names the CR limit `--max-concurrent-updaters` (env `MAX_CONCURRENT_UPDATERS`).

Leader election: `--leader-election` ensures one active controller manager. `--leader-election-namespace` sets the lease namespace; empty means the pod's own namespace, and it must be set when running locally.

Trap: the `argocd-image-updater-leader-election-role` Role and RoleBinding are created only in the controller's own namespace by the install manifests. If the lease namespace is any other, create them there by hand or the controller cannot acquire the lease. Adding a namespace to `--watch-namespaces` does not create them.

## Checked

2026-11-08. Read in full: docs/install/cmd/run.md and docs/install/cmd/webhook.md (for the --max-concurrent-updaters flag). Confirmed the interval default, unit handling, zero value and precedence, the concurrency flags and environment variables, and the leader election namespace and RBAC warning. Removed: the closing claim that a longer interval reduces registry and GitHub API load, which the docs do not state.

Method: documentation only; no commands were run.
