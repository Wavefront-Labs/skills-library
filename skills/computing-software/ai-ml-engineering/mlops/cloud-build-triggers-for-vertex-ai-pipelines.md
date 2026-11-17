---
id: computing-software.ai-ml-engineering.mlops.cloud-build-triggers-for-vertex-ai-pipelines
name: cloud-build-triggers-for-vertex-ai-pipelines
category: computing-software
field: ai-ml-engineering
product: mlops
tags: [mlops, cloud-build, vertex-ai-pipelines, ci-cd, kfp, artifact-registry]
level: practitioner
status: draft
description: "Wire Cloud Build triggers that test, compile and publish Kubeflow pipelines to Artifact Registry and submit Vertex AI pipeline runs with a dedicated service account."
sources:
  - https://cloud.google.com/build/docs/automating-builds/create-manage-triggers
  - https://cloud.google.com/vertex-ai/docs/pipelines/create-pipeline-template
  - https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cloud Build triggers for Vertex AI pipelines

**Goal:** a merge to main tests the pipeline code, compiles it, publishes a versioned template, and (optionally) runs it on Vertex AI without anyone running notebooks.

## cloudbuild.yaml
```yaml
steps:
- id: test
  name: python:3.11
  entrypoint: bash
  args: ["-c", "pip install -r requirements.txt && pytest -q tests/"]
- id: build-image
  name: gcr.io/cloud-builders/docker
  args: ["build", "-t", "${_REGION}-docker.pkg.dev/$PROJECT_ID/ml/trainer:$SHORT_SHA", "trainer/"]
- id: push-image
  name: gcr.io/cloud-builders/docker
  args: ["push", "${_REGION}-docker.pkg.dev/$PROJECT_ID/ml/trainer:$SHORT_SHA"]
- id: compile-and-publish
  name: python:3.11
  entrypoint: bash
  args: ["-c", "pip install -r requirements.txt && python ci/publish.py --image-tag $SHORT_SHA"]
substitutions:
  _REGION: us-central1
options:
  logging: CLOUD_LOGGING_ONLY
```
`ci/publish.py`:
```python
from kfp import compiler
from kfp.registry import RegistryClient
from google.cloud import aiplatform
compiler.Compiler().compile(pipeline_func=train_pipeline, package_path="pipeline.yaml")
rc = RegistryClient(host=f"https://{REGION}-kfp.pkg.dev/{PROJECT}/pipelines")
name, version = rc.upload_pipeline(file_name="pipeline.yaml", tags=[IMAGE_TAG, "latest"])
aiplatform.init(project=PROJECT, location=REGION)
aiplatform.PipelineJob(display_name="train", template_path=f"https://{REGION}-kfp.pkg.dev/{PROJECT}/pipelines/{name}/{IMAGE_TAG}",
                       pipeline_root=ROOT, parameter_values={"trainer_image_tag": IMAGE_TAG}).submit(service_account=PIPELINE_SA)
```
Pin the component image by the commit tag so the template and code version match.

## Trigger
```bash
gcloud builds triggers create github --name=ml-pipeline-main \
  --repo-owner=acme --repo-name=churn --branch-pattern='^main$' \
  --build-config=cloudbuild.yaml --included-files='pipelines/**,trainer/**' \
  --service-account=projects/$PROJECT/serviceAccounts/cloudbuild-ml@$PROJECT.iam.gserviceaccount.com
```
Add a pull-request trigger running only `test` and compile (no submit) for review feedback.

## Permissions
- Build SA: Artifact Registry writer, Vertex AI user, `iam.serviceAccountUser` on the pipeline SA only.
- Pipeline SA: data read, model registry write, nothing else. Never run pipelines as the default compute SA.

## Gotchas
- `$SHORT_SHA` is empty for manual runs without a commit; pass a substitution or use `$BUILD_ID`.
- Default build timeout (10 min) is too short for large images; set `timeout:`.
- Submitting a long pipeline from the build is fine (submit is async); waiting on it holds a build worker.

## Verify
- [ ] Merge to main publishes a template tagged with the commit.
- [ ] The Vertex run's component images carry the same tag.
- [ ] PR builds never submit pipeline runs.
