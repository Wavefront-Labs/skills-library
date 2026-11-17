---
id: computing-software.devops-ci-cd.argocd-image-updater.webhook-enable-ports-and-exposure
name: webhook-enable-ports-and-exposure
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, webhook, enable-webhook, webhook-port, healthz, ratelimit, network-policy]
level: practitioner
status: docs-checked
description: "Turn on the registry webhook server with run or standalone, with default ports, endpoints, ConfigMap keys, rate limit and how to expose it."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enabling and exposing the webhook server

Webhooks let registries trigger an immediate update check and reduce polling load.

Two ways:

- with polling: `argocd-image-updater run --enable-webhook --webhook-port [PORT]` (default port `8082`; env `ENABLE_WEBHOOK`, `WEBHOOK_PORT`; ConfigMap `webhook.enable: true`, `webhook.port`)
- webhook only: `argocd-image-updater webhook --webhook-port [PORT]` (default port `8080`); change the Deployment container `args` to `webhook`

Endpoints: `/webhook` receives notifications and `/healthz` reports liveness. Errors are returned in the response body: "no handler available for this webhook" means the `type` query parameter is missing or wrong; "Missing/invalid webhook secret" means secrets are not configured properly.

Rate limit: `--webhook-ratelimit-allowed` (env `WEBHOOK_RATELIMIT_ALLOWED`, ConfigMap `webhook.ratelimit-allowed`). The default `0` disables it; over the limit requests wait. The flag text says allowed requests per hour while the ConfigMap comment says per second; the docs disagree.

Exposure: a Service and Ingress ship in the `config/networking` directory and are not part of `install.yaml`. The Service exposes port 8080 and forwards to controller port 8082. The default NetworkPolicy needs the source namespace labelled `kubectl label namespace <namespace> webhooks=enabled`; update the policy port if you change `webhook.port`.

Other `webhook` command flags: `--max-concurrent-apps`, `--max-concurrent-updaters`, `--argocd-namespace` and the git commit options.

## Checked

2026-11-08. Read in full: docs/configuration/webhook.md, docs/install/cmd/webhook.md and docs/install/cmd/run.md. Confirmed ports 8082 (run) and 8080 (webhook command), the ConfigMap keys, the endpoints, the error messages, the rate limit default of 0, the config/networking manifests, the Service port mapping and the NetworkPolicy label. Corrected: --max-concurrent-updaters belongs to the webhook command (run uses --max-concurrent-reconciles), so the flags are no longer called shared with run; the vague 'check the behaviour' advice was replaced by the stated doc discrepancy.

Method: documentation only; no commands were run.
