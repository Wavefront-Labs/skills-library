---
id: computing-software.ai-ml-engineering.mlflow.mlflow-ai-gateway-routes
name: mlflow-ai-gateway-routes
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-genai, mlflow-ai-gateway, llm-gateway, rate-limiting, provider-abstraction, api-key-management]
level: practitioner
status: docs-checked
description: "Centralize LLM access with the MLflow AI Gateway built into the tracking server: LLM connections, endpoints, invocation APIs, traffic splits, fallbacks and budgets."
sources:
  - https://mlflow.org/docs/latest/genai/governance/ai-gateway/
  - https://mlflow.org/docs/latest/genai/governance/ai-gateway/quickstart/
  - https://mlflow.org/docs/latest/genai/governance/ai-gateway/endpoints/query-endpoints/
  - https://mlflow.org/docs/latest/genai/governance/ai-gateway/traffic-routing-fallbacks/
  - https://mlflow.org/docs/latest/genai/governance/ai-gateway/budget-alerts-limits/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow AI Gateway endpoints
**Goal:** one internal entry point for LLM access: provider keys held centrally, providers swappable by endpoint configuration, spend controlled by policy.
## Setup
The AI Gateway is built into the MLflow tracking server. It needs the `genai` extra, a SQL backend store and the FastAPI tracking server (the default for `mlflow server`).
```bash
pip install 'mlflow[genai]'
mlflow server --port 5000
```
1. Create an **LLM connection** (an encrypted, reusable provider API key) in the UI: `/#/settings`, LLM Connections tab.
2. Create an **endpoint** in the UI: `/#/gateway`. Pick a name (it becomes the path `/gateway/<endpoint-name>/...`), a provider, a model and the connection. Common providers are listed first, and a LiteLLM catalogue is available if LiteLLM is installed separately.
## Call it
```bash
curl -X POST http://localhost:5000/gateway/my-chat-endpoint/mlflow/invocations \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
```
- Unified APIs: `POST /gateway/{endpoint_name}/mlflow/invocations` (chat and embeddings), OpenAI-compatible `POST /gateway/mlflow/v1/chat/completions` (endpoint name as `model`) and `GET /gateway/mlflow/v1/models`. With the OpenAI Python client use `base_url="http://localhost:5000/gateway/mlflow/v1"`.
- Passthrough APIs keep provider-native formats, for example `POST /gateway/anthropic/v1/messages` and `POST /gateway/openai/v1/chat/completions`.
## Routing and budgets
- Traffic split: per-model weights from 1% to 100% that must sum to exactly 100%, for A/B tests and gradual migration.
- Fallbacks: an ordered list tried from top to bottom when the primary model errors or is rate limited.
- Budget policies: a USD threshold over a daily, weekly or monthly window with action **Alert** (webhook, fired once per window) or **Reject** (requests arriving after the threshold is exceeded get HTTP 429).
- Custom provider base URLs must be HTTPS and must not resolve to private, loopback or link-local addresses unless you set `MLFLOW_GATEWAY_API_BASE_ALLOW_PRIVATE_IPS=true` (and `MLFLOW_GATEWAY_API_BASE_ALLOWED_SCHEMES=http,https` for non-TLS servers).
## Legacy file-based gateway
`mlflow gateway start --config-path gateway.yaml` (YAML route definitions) still exists in the CLI but is marked deprecated in favour of the UI-based AI Gateway. Migrate each route to an LLM connection plus an endpoint.
## Why a gateway
- Applications never see provider keys; rotating a key means editing one LLM connection.
- Switching an endpoint from one model or provider to another is a configuration change (re-run evals first).
## Gaps to cover yourself
The gateway is served by the tracking server, so put the same network and authentication controls in front of it as for the rest of MLflow, and keep your own PII controls on prompts.
## Verify
- [ ] Client code contains no provider API keys.
- [ ] A Reject budget policy returns 429 once the threshold is exceeded.
- [ ] Endpoint swap tested with the eval suite before switching production traffic.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- Gateway built into the tracking server, `mlflow[genai]`, SQL backend and FastAPI requirement, UI paths `/#/settings` and `/#/gateway`: docs/genai/governance/ai-gateway/quickstart.mdx and endpoints/create-and-manage.mdx.
- Invocation, OpenAI-compatible, models-list and passthrough paths: endpoints/query-endpoints.mdx.
- Traffic split weights (1-100, sum 100) and ordered fallbacks: traffic-routing-fallbacks.mdx. Budget Alert/Reject, 429, once-per-window alert: budget-alerts-limits.mdx. Base-URL validation and the two env vars: api-keys/create-and-manage.mdx.
- `mlflow gateway start` still has `--config-path`, `--host`, `--port`, `--workers` but is decorated as deprecated in favour of the UI gateway: mlflow/gateway/cli.py.
- Removed as unconfirmed: the YAML-per-route rate-limit (`limit: calls/renewal_period`) examples, hot reload of the config file, the `get_deploy_client("http://gateway:7000")` call and a pinned provider model name. The setup page links in the old sources are replaced by the current ones.

Method: documentation only; no commands were run.
