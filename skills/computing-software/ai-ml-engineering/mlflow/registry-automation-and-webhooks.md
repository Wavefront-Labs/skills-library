---
id: computing-software.ai-ml-engineering.mlflow.registry-automation-and-webhooks
name: registry-automation-and-webhooks
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, model-registry, registry-webhooks, model-version-created, ci-cd, automation, deployment-jobs, search-model-versions]
level: practitioner
status: docs-checked
description: "Trigger validation and deployment when new MLflow model versions or aliases appear: MLflow webhooks with signature checks, platform-managed options, and polling fallbacks."
sources:
  - https://mlflow.org/docs/latest/self-hosting/webhooks/
  - https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Registry automation and webhooks

**Goal:** a new model version automatically gets validated, and an approved alias change automatically deploys - no one runs scripts by hand.

## Event sources
1. **MLflow webhooks** (self-hosting docs): `MlflowClient().create_webhook(name=..., url=..., events=["model_version.created"], secret=...)` registers an HTTP endpoint. Events are `registered_model.created`, `model_version.created`, `model_version_tag.set`, `model_version_tag.deleted`, `model_version_alias.created` and `model_version_alias.deleted`. `test_webhook` sends a test event. The JSON payload has `entity`, `action`, `timestamp`, `data` (and `workspace` when workspaces are enabled).
2. **Platform-managed automation** (for example Databricks deployment jobs): defined by the platform's own documentation, which this skill does not cover.
3. **Polling fallback** (works everywhere): a scheduled CI job queries the registry:
```python
from mlflow import MlflowClient
c = MlflowClient()
new = c.search_model_versions("name='churn' and tags.validated = 'pending'")
for mv in new:
    trigger_validation(mv.name, mv.version)
```

## Webhook receiver essentials
- Verify the signature before acting: with a secret, MLflow signs each request with HMAC-SHA256 and sends it in the `X-MLflow-Signature` header as `v1,<base64 signature>`. Check the `X-MLflow-Timestamp` header (Unix time) and reject requests that are too old (the docs suggest older than 5 minutes).
- Respond fast (200) and enqueue the work - don't run a 20-minute evaluation inside the HTTP handler. Failed deliveries are retried (`MLFLOW_WEBHOOK_REQUEST_MAX_RETRIES`, default 3).
- Idempotency: the same event can arrive twice; key work by `(model, version, event)` and skip duplicates.
- Typical receiver: a small service or a CI `repository_dispatch` trigger (GitHub Actions) carrying model name and version.

## Pipeline shape
`version created` -> validation job (metrics vs champion, slices, latency, signature check) -> tag `validated=passed|failed` -> (human approval if required) -> alias `champion` set -> `alias changed` event -> deploy job updates serving.

Separate validation from deployment so a human gate can sit between them.

## Verify
- [ ] Registering a test version triggers validation within minutes.
- [ ] Forged/unsigned webhook requests rejected.
- [ ] Duplicate events don't trigger duplicate deployments.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Webhook events, `create_webhook`/`test_webhook`, `X-MLflow-Signature` (`v1,<base64>`, HMAC-SHA256), `X-MLflow-Timestamp`, payload fields, `MLFLOW_WEBHOOK_REQUEST_MAX_RETRIES` default 3: docs/self-hosting/webhooks/index.mdx (the old `ml/webhooks` page redirects there).
- `search_model_versions` filter identifiers (`name`, `source_path`, `run_id`, `tags.<key>`), comparators and `AND`: MlflowClient docstring.
- Databricks deployment jobs were removed from the skill body: Databricks documentation is not published in a public repository.

Method: documentation only; no commands were run.
