---
id: computing-software.ai-ml-engineering.mlflow.databricks-model-serving-endpoints
name: databricks-model-serving-endpoints
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, databricks-model-serving, model-serving, serving-endpoints, unity-catalog, scale-to-zero]
level: practitioner
status: draft
description: "Deploy MLflow models to Databricks Model Serving: endpoint config via SDK or REST, traffic splits, scale-to-zero, secrets, inference tables and querying."
sources:
  - https://docs.databricks.com/aws/en/machine-learning/model-serving/create-manage-serving-endpoints
  - https://docs.databricks.com/aws/en/machine-learning/model-serving/score-custom-model-endpoints
  - https://docs.databricks.com/aws/en/ai-gateway/inference-tables
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Databricks Model Serving endpoints

**Goal:** a Unity Catalog model version serves real-time traffic with controlled rollout, right-sized compute and logged requests.

## Create
```python
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointCoreConfigInput, ServedEntityInput, TrafficConfig, Route
w = WorkspaceClient()
w.serving_endpoints.create_and_wait(
    name="churn",
    config=EndpointCoreConfigInput(
        served_entities=[
            ServedEntityInput(name="v7", entity_name="prod.ml.churn", entity_version="7",
                              workload_size="Small", scale_to_zero_enabled=False,
                              environment_vars={"FEATURE_API_KEY": "{{secrets/ml/feature_api_key}}"}),
            ServedEntityInput(name="v8", entity_name="prod.ml.churn", entity_version="8",
                              workload_size="Small", scale_to_zero_enabled=False),
        ],
        traffic_config=TrafficConfig(routes=[Route(served_model_name="v7", traffic_percentage=90),
                                             Route(served_model_name="v8", traffic_percentage=10)]),
    ),
)
```
The same config is a JSON body for `POST /api/2.0/serving-endpoints`, or `mlflow.deployments.get_deploy_client("databricks").create_endpoint(...)`. Keep it in a Databricks Asset Bundle so it is versioned.

## Sizing
- `workload_size` Small/Medium/Large maps to concurrency ranges; `workload_type` selects CPU or GPU classes.
- `scale_to_zero_enabled=True` saves cost for dev and low-traffic endpoints but the first request after idle waits for a cold start (minutes for large models). Keep it off for latency SLAs.
- Endpoint creation builds a container from the model's logged environment; dependency errors surface in the build logs, not at query time.

## Query
```bash
curl -X POST "$HOST/serving-endpoints/churn/invocations" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" -d '{"dataframe_split": {"columns": ["tenure","plan"], "data": [[12,"pro"]]}}'
```
Also accepted: `dataframe_records`, `inputs` (tensor), and chat/completions payloads for LLM models.

## Rollout
Update traffic percentages with `w.serving_endpoints.update_config(...)` in steps (10 -> 50 -> 100), watching latency and error metrics per served entity, then remove the old entity. Updates are zero-downtime but a failed config update leaves the previous config serving.

## Observability
Enable AI Gateway inference tables to log requests and responses to a UC Delta table; join with labels later for monitoring. Endpoint metrics (latency, QPS, errors, CPU/GPU) are on the endpoint page and exportable.

## Verify
- [ ] Endpoint state READY and both entities receive the configured traffic share.
- [ ] Secrets are referenced via `{{secrets/...}}`, not literal values.
- [ ] Inference table receives rows within minutes of traffic.
