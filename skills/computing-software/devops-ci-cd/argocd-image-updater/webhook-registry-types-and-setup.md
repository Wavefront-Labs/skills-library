---
id: computing-software.devops-ci-cd.argocd-image-updater.webhook-registry-types-and-setup
name: webhook-registry-types-and-setup
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, webhook, webhook-type, aliyun-acr, azure-acr, cloudevents, aws-ecr, eventbridge]
level: advanced
status: docs-checked
description: "Set the webhook URL type per registry (docker.io, ghcr.io, harbor, quay.io, aliyun-acr, acr, cloudevents) and wire AWS ECR through EventBridge."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/webhook.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/cmd/webhook.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Webhook URL types and registry setup

URL pattern: `https://app1.example.com/webhook?type=<TYPE>`

| Registry | `type` |
|---|---|
| Docker Hub | `docker.io` |
| GitHub Container Registry | `ghcr.io` |
| Harbor | `harbor` |
| Quay | `quay.io` |
| Aliyun ACR | `aliyun-acr` |
| Azure ACR | `acr` |
| AWS ECR (CloudEvents) | `cloudevents` |

Aliyun ACR: the payload lacks the instance name, so when the endpoint is not `registry.<region>.aliyuncs.com` add `&registry_url=my-instance-registry.cn-shanghai.cr.aliyuncs.com`.

Azure ACR: registry host, repository, tag and digest are read from `request.host`, `target.repository`, `target.tag`, `target.digest`; only `action: push` events are processed and an empty tag is handled.

AWS ECR has no built-in webhook support, so EventBridge converts push events to CloudEvents. Steps: create a rule for ECR push events, an Input Transformer, an API Destination for the webhook, and IAM permissions. Input paths map `id`, `time`, `account`, `region`, `$.detail.repository-name`, `$.detail.image-digest`, `$.detail.image-tag`; the template builds `specversion: "1.0"`, `type: com.amazon.ecr.image.push`, `source: urn:aws:ecr:<region>:<account>:repository/<repo>` and `data` with camelCase `repositoryName`, `imageDigest`, `imageTag`, `registryId`. Webhook URL: `.../webhook?type=cloudevents&secret=<YOUR_SECRET>` or the `X-Webhook-Secret` header. Terraform lives in `config/examples/cloudevents/terraform/`.

## Checked

2026-11-08. Read in full: docs/configuration/webhook.md and docs/install/cmd/webhook.md. Confirmed the type value per registry, the Aliyun registry_url parameter, the ACR payload fields and push-only handling, and the EventBridge input paths, template, URL and Terraform directory. Reworded the ECR claim to match the docs (no built-in webhook support).

Method: documentation only; no commands were run.
