---
id: computing-software.devops-ci-cd.argocd-image-updater.run-logging-dry-run-and-probes
name: run-logging-dry-run-and-probes
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, loglevel, logformat, dry-run, health-probe, kube-events, run-flags]
level: practitioner
status: docs-checked
description: "Operate the run command: --dry-run, --loglevel and --logformat, --disable-kube-events, and the health probe address behind probes."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Logging, dry run and health probes

Flags on `argocd-image-updater run`:

- `--dry-run`: Image Updater does not change any workload it finds in need of an upgrade. Use it to preview behaviour on a real cluster.
- `--loglevel <level>`: `trace`, `debug`, `info`, `warn` or `error` (env `IMAGE_UPDATER_LOGLEVEL`). The ConfigMap key `log.level` in `argocd-image-updater-config` does the same; the default is `info`.
- `--logformat <format>`: `text` or `json` (env `IMAGE_UPDATER_LOGFORMAT`).
- `--disable-kube-events`: stop emitting Kubernetes events (env `IMAGE_UPDATER_KUBE_EVENTS`).
- `--health-probe-bind-address <port>`: local port of the health server used for health and readiness probes when running as a workload; `0` disables it.
- `--metrics-bind-address <port>`: metrics server port, `0` (default) disables it.
- `--metrics-secure`: serve metrics over HTTPS; use `--metrics-secure="false"` for plain HTTP.
- `--enable-http2`: enable HTTP/2 for the metrics and webhook servers.
- `--warmup-cache`: warm the cache at startup (default true).

The installation guide recommends setting the log level explicitly and using more verbose logging during first steps to help troubleshooting. `--once` sets the probe address to 0, which disables the health server.

## Checked

2026-11-08. Read in full: docs/install/cmd/run.md and docs/install/installation.md. Confirmed every flag, environment variable and default listed, the log.level ConfigMap key with its info default, and the --once behaviour. Removed: the claim that debug logging shows tag filtering and platform decisions.

Method: documentation only; no commands were run.
