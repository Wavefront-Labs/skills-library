---
id: computing-software.devops-ci-cd.argocd-image-updater.prometheus-metrics
name: prometheus-metrics
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, metrics, prometheus, metrics-bind-address, grafana, observability]
level: practitioner
status: docs-checked
description: "Enable and read Argo CD Image Updater Prometheus metrics: the four per-CR series, labels, --metrics-bind-address and unpopulated series."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/installation.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Prometheus metrics

Metrics are disabled by default: `--metrics-bind-address` defaults to "0", which disables the metrics server. Enable them by giving a port (for example `:8080`); they are served on `/metrics`. `--metrics-secure` controls whether the endpoint is served over HTTPS; use `--metrics-secure="false"` for plain HTTP. HTTP/2 for the metrics and webhook servers needs `--enable-http2`.

CR-scoped series carry the labels `image_updater_cr_name` and `image_updater_cr_namespace`:

- `argocd_image_updater_applications_watched_total` (gauge): applications watched per ImageUpdater CR
- `argocd_image_updater_images_watched_total` (gauge): images considered for update per CR
- `argocd_image_updater_images_updated_total` (counter): images updated per CR
- `argocd_image_updater_images_errors_total` (counter): errors during image updates per CR

Gauges reflect the last run; counters are cumulative since controller start.

These series are populated only when the controller polls (the default `run` command). In webhook-only mode (`webhook` command) they are disabled so that deleted CRs do not leave orphaned series.

Defined but unreliable (may be absent or always `0`): `argocd_image_updater_k8s_api_requests_total`, `argocd_image_updater_k8s_api_errors_total`, `argocd_image_updater_registry_requests_total`, `argocd_image_updater_registry_requests_failed_total`.

A very rudimentary Grafana dashboard definition ships in the repository `config` directory.

## Checked
2026-11-08. Confirmed against the Argo CD Image Updater installation page (Metrics section) and the run command page: `--metrics-bind-address` default "0" and `:8080` example, `/metrics`, `--metrics-secure` and `--enable-http2`, the CR labels, the four series and their types, polling-only population and webhook-mode behaviour, the four defined-but-unpopulated series and the sample Grafana dashboard. Nothing removed.
Method: documentation only; no commands were run.
