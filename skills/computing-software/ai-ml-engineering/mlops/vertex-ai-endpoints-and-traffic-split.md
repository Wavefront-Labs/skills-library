---
id: computing-software.ai-ml-engineering.mlops.vertex-ai-endpoints-and-traffic-split
name: vertex-ai-endpoints-and-traffic-split
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, vertex-ai-endpoints, traffic-split, vertex-ai, canary-deployment, online-prediction]
level: practitioner
status: draft
description: "Deploy models to Vertex AI endpoints with machine and replica settings, split traffic between deployed models for canaries, roll back, and undeploy safely."
sources:
  - https://cloud.google.com/vertex-ai/docs/general/deployment
  - https://cloud.google.com/vertex-ai/docs/predictions/get-online-predictions
  - https://cloud.google.com/python/docs/reference/aiplatform/latest/google.cloud.aiplatform.Endpoint
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Vertex AI endpoints and traffic split

**Goal:** a new model version receives a controlled slice of live traffic on the same endpoint, and rollback is one command.

## Deploy
```python
from google.cloud import aiplatform
aiplatform.init(project=PROJECT, location="us-central1")
endpoint = aiplatform.Endpoint.create(display_name="churn")      # once
model_v2 = aiplatform.Model(f"projects/{PROJECT}/locations/us-central1/models/churn@2")
model_v2.deploy(endpoint=endpoint, deployed_model_display_name="churn-v2",
                machine_type="n1-standard-4", min_replica_count=2, max_replica_count=6,
                autoscaling_target_cpu_utilization=60, traffic_percentage=10,
                service_account=SERVING_SA)
```
`traffic_percentage=10` gives the new deployment 10% and scales existing deployments down proportionally. Each deployed model has its own replicas, so a canary costs full minimum replicas.

## Adjust and roll back
```python
ids = {d.display_name: d.id for d in endpoint.list_models()}
endpoint.update(traffic_split={ids["churn-v1"]: 50, ids["churn-v2"]: 50})
endpoint.update(traffic_split={ids["churn-v1"]: 100, ids["churn-v2"]: 0})    # rollback
endpoint.undeploy(deployed_model_id=ids["churn-v2"])                          # when done
```
gcloud: `gcloud ai endpoints update ENDPOINT --region=us-central1 --traffic-split=ID1=90,ID2=10`. Traffic values must sum to 100. You cannot undeploy a model that still has traffic; move traffic first.

## Prediction
```python
endpoint.predict(instances=[{"tenure": 12, "plan": "pro"}])
```
Response includes `deployed_model_id`, so you can attribute predictions to versions in logs. Enable request-response logging to BigQuery for monitoring and offline comparison.

## Production options
- Dedicated or private endpoints (VPC peering / Private Service Connect) for lower latency and no public exposure.
- GPUs: `accelerator_type`, `accelerator_count`; scale on `autoscaling_target_accelerator_duty_cycle`.
- Custom containers must serve the health and predict routes Vertex expects (`AIP_HEALTH_ROUTE`, `AIP_PREDICT_ROUTE`, port `AIP_HTTP_PORT`).
- Traffic split is random per request; for sticky per-user experiments route in your application.

## Verify
- [ ] Logged `deployed_model_id` share matches the configured split.
- [ ] Error rate and latency compared per deployed model before each increase.
- [ ] Rollback rehearsed: traffic to previous version within minutes.
