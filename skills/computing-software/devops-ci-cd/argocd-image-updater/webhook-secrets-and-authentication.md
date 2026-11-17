---
id: computing-software.devops-ci-cd.argocd-image-updater.webhook-secrets-and-authentication
name: webhook-secrets-and-authentication
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, webhook, webhook-secret, webhook-require-secret, argocd-image-updater-secret, query-secret, authorization-header]
level: advanced
status: docs-checked
description: "Secure registry webhooks: per-registry secrets, built-in versus query-parameter delivery, and webhook-require-secret defaulting to true."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/run.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhook secrets and authentication

Secrets live in the `argocd-image-updater-secret` Secret:

```yaml
stringData:
  webhook.docker-secret: <YOUR_SECRET>
  webhook.ghcr-secret: <YOUR_SECRET>
  webhook.harbor-secret: <YOUR_SECRET>
  webhook.quay-secret: <YOUR_SECRET>
  webhook.aliyun-acr-secret: <YOUR_SECRET>
  webhook.acr-secret: <YOUR_SECRET>
  webhook.cloudevents-secret: <YOUR_SECRET>
```

Flags/env: `--docker-webhook-secret` (`DOCKER_WEBHOOK_SECRET`), `--ghcr-webhook-secret`, `--harbor-webhook-secret`, `--quay-webhook-secret`, `--aliyun-acr-webhook-secret`, `--acr-webhook-secret`, `--cloudevents-webhook-secret` with the matching `*_WEBHOOK_SECRET` variables.

Two delivery methods:

- registries with built-in secret support: GitHub Container Registry, Harbor and Azure ACR (configure per the registry's docs; for ACR set an `Authorization` header with `az acr webhook update -n <webhook> -r <registry> --headers "Authorization=<YOUR_SECRET>"`, compared in constant time)
- parameter secrets, for registries without them: `https://app1.example.com/webhook?type=<TYPE>&secret=<YOUR_SECRET>` for Docker Hub, Quay, Aliyun ACR and AWS ECR via CloudEvents. It is a small extra layer, not strong security; never reuse a secret shared with critical services. It cannot be used if the registry has its own method. CloudEvents also accepts an `X-Webhook-Secret` header.

Breaking change: `--webhook-require-secret` (env `WEBHOOK_REQUIRE_SECRET`) defaults to `true`, so only handlers with a configured secret are registered and others reject requests. Set `false` only in local development or isolated networks; it removes authentication on every handler without a secret.

## Checked

2026-11-08. Read in full: docs/configuration/webhook.md, docs/install/cmd/webhook.md and docs/install/cmd/run.md of argoproj-labs/argocd-image-updater. Confirmed the secret keys in argocd-image-updater-secret, the flags and environment variables, which registries use built-in secrets versus the query parameter, the ACR Authorization header, the X-Webhook-Secret header and the webhook-require-secret default. Nothing removed.

Method: documentation only; no commands were run.
