---
id: computing-software.ai-ml-engineering.mlflow.deploying-mlflow-models-to-sagemaker-and-kserve
name: deploying-mlflow-models-to-sagemaker-and-kserve
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, mlflow-deployment, mlflow-sagemaker, mlserver, kserve, v2-inference-protocol, model-serving]
level: practitioner
status: docs-checked
description: "Deploy MLflow models to SageMaker and to Kubernetes via KServe: deployment client config, deployment modes, ECR image push, Open Inference Protocol payloads and canary rollout."
sources:
  - https://mlflow.org/docs/latest/ml/deployment/deploy-model-to-sagemaker/
  - https://github.com/mlflow/mlflow/blob/master/mlflow/sagemaker/__init__.py
  - https://github.com/mlflow/mlflow/blob/master/CHANGELOG.md
  - https://github.com/kserve/website/blob/main/docs/model-serving/predictive-inference/frameworks/mlflow/mlflow.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploying MLflow models to SageMaker and Kubernetes

**Goal:** take a registered MLflow model to a managed endpoint or a Kubernetes inference service with the same artifact.

## SageMaker
```bash
mlflow sagemaker build-and-push-container -m models:/churn/7     # builds a SageMaker-compatible image and pushes it to ECR
```
```python
from mlflow.deployments import get_deploy_client
client = get_deploy_client("sagemaker:/us-east-1")
client.create_deployment(
    name="churn-prod",
    model_uri="models:/churn/7",
    config={"execution_role_arn": role_arn, "instance_type": "ml.m5.large", "instance_count": 2,
            "image_url": ecr_image_uri, "region_name": "us-east-1",
            "archive": False, "synchronous": True},
)
client.predict("churn-prod", df_sample)
```
- `update_deployment` with a new `model_uri` replaces the existing model by default. The deployment modes are `create` (fails if the application exists), `replace` and `add`; `add` attaches the model to the existing endpoint with an initial traffic weight of zero, so route traffic to it yourself (AWS console or `UpdateEndpointWeightsAndCapacities`).
- MLflow uploads the pyfunc model to S3 and the endpoint downloads it from there. `execution_role_arn` needs access to the image and the bucket; the bucket defaults to a SageMaker-compatible name unless you set `bucket`.
- With `archive=False`, replaced endpoint configurations and models are deleted, and that requires `synchronous=True`.

## Kubernetes with KServe
MLServer is no longer an MLflow serving backend: the `enable_mlserver` option was removed in MLflow 3.13.0, so `mlflow models build-docker` and `mlflow models serve` always use MLflow's built-in scoring server. To serve through KServe, let KServe pull the model artifact directly:
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata: {name: churn}
spec:
  predictor:
    model:
      modelFormat: {name: mlflow}
      protocolVersion: v2
      storageUri: s3://mlflow-artifacts/1/<run_id>/artifacts/model
```
Open Inference Protocol (v2) request, as in KServe's MLflow example:
```json
{"parameters": {"content_type": "pd"},
 "inputs": [{"name": "fixed acidity", "shape": [1], "datatype": "FP32", "data": [7.4]}]}
```
POST to `/v2/models/<inference-service-name>/infer` (here `/v2/models/churn/infer`). Inputs are named per signature column.

## Choosing
SageMaker: MLflow builds the image, uploads the model and creates the endpoint; you pay per endpoint instance. KServe: canary traffic split with `canaryTrafficPercent` on the predictor; you run the cluster.

## Verify
- [ ] Endpoint predictions equal local pyfunc predictions on a sample.
- [ ] Rollout to a new version tested with rollback.
- [ ] Endpoint metadata records the registry version deployed.

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- SageMaker flow (`build-and-push-container`, `create_deployment`, S3 upload, IAM role needs): docs/classic-ml/deployment/deploy-model-to-sagemaker/index.mdx.
- `create_deployment` config keys `execution_role_arn`, `bucket`, `image_url`, `region_name`, `archive`, `instance_type`, `instance_count`, `synchronous`, and the create/replace/add modes with the zero-weight note on `add`: mlflow/sagemaker/__init__.py docstrings.
- MLServer removal (`enable_mlserver` removed, 3.13.0 breaking change) and the earlier deprecation: CHANGELOG.md; no `--enable-mlserver` option exists in mlflow/models/cli.py.
- KServe `InferenceService` with `modelFormat: mlflow`, `protocolVersion: v2`, `storageUri`, the `/v2/models/<name>/infer` path and the v2 request shape: kserve/website docs/model-serving/predictive-inference/frameworks/mlflow/mlflow.md and mlflow-input.json (repo last pushed 2026-10-20). `canaryTrafficPercent` on the predictor: kserve rollout-strategies/canary-example.md.
- Removed as unconfirmed: the once-per-MLflow-version image claim, INT64/BYTES datatype example, and KServe scale-to-zero and shared-GPU claims. The Kubernetes deployment page of the MLflow docs now redirects to the self-hosting guide, so the dead link was replaced.

Method: documentation only; no commands were run.
