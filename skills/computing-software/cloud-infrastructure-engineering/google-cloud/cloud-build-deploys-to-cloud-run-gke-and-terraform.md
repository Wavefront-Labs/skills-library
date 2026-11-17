---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-deploys-to-cloud-run-gke-and-terraform
name: cloud-build-deploys-to-cloud-run-gke-and-terraform
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-build, cloud-build-cloud-run-deploy, cloud-build-gke-deploy, build-deploy-gke, terraform-in-cloud-build, cloud-build-terraform, private-pools]
level: practitioner
status: docs-checked
description: "Write cloudbuild.yaml pipelines that deploy to Cloud Run and GKE by digest and run Terraform plan on PRs and apply on merge, with the right build service account permissions."
sources: ["https://cloud.google.com/build/docs/deploying-builds/deploy-cloud-run", "https://cloud.google.com/build/docs/deploying-builds/deploy-gke", "https://cloud.google.com/docs/terraform/resource-management/managing-infrastructure-as-code", "https://cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Build deploys to Cloud Run, GKE and Terraform

## 1. Build once, deploy to Cloud Run
```yaml
steps:
- id: build
  name: gcr.io/cloud-builders/docker
  args: [build, -t, '${_IMG}:$SHORT_SHA', .]
- id: push
  name: gcr.io/cloud-builders/docker
  args: [push, '${_IMG}:$SHORT_SHA']
- id: deploy-run
  name: gcr.io/google.com/cloudsdktool/cloud-sdk:slim
  entrypoint: gcloud
  args: [run, deploy, orders, '--image=${_IMG}:$SHORT_SHA', --region=europe-west2, --quiet]
substitutions: {_IMG: europe-west2-docker.pkg.dev/$PROJECT_ID/apps/orders}
serviceAccount: projects/$PROJECT_ID/serviceAccounts/cb-deployer@$PROJECT_ID.iam.gserviceaccount.com
options: {logging: CLOUD_LOGGING_ONLY}
```
The Cloud Build page lists Cloud Run Admin (`roles/run.admin`) to deploy services and Service Account User on the runtime service account; grant the narrowest roles that work and verify them against the IAM roles reference.

## 2. GKE
```yaml
- id: deploy-gke
  name: gcr.io/cloud-builders/gke-deploy
  args: [run, --filename=k8s/, '--image=${_IMG}:$SHORT_SHA', --location=europe-west2, --cluster=prod-eu, --namespace=orders]
```
`gke-deploy` wraps kubectl: it updates the resource file to use the image digest instead of a tag, applies it, and waits for the resources to be ready. The build service account needs permission to deploy to the cluster.

## 3. Terraform
```yaml
steps:
- name: hashicorp/terraform:<VERSION>
  dir: envs/prod
  args: [init, -input=false]
- name: hashicorp/terraform:<VERSION>
  dir: envs/prod
  args: [plan, -input=false, -out=tfplan]
- name: hashicorp/terraform:<VERSION>
  dir: envs/prod
  entrypoint: sh
  args: [-c, 'if [ "$BRANCH_NAME" = "main" ]; then terraform apply -input=false tfplan; fi']
```
Triggers: PR trigger → plan only (comment the plan back via a step if desired); push to `main` → apply.
Store Terraform state in a Cloud Storage bucket. The Terraform service account holds the roles the code manages (often broad), so protect the apply trigger with required approval.

## Gotchas
- Without a user-managed service account Cloud Build uses the default Cloud Build service account, which may have unnecessarily broad permissions. Set `serviceAccount:` explicitly and a `logging` option: with a user-specified service account, logs must go to a user-owned Cloud Storage bucket or a Cloud Logging bucket (`CLOUD_LOGGING_ONLY` or `GCS_ONLY` with `logsBucket`).
- Use one trigger per environment so applies on the same state do not overlap.

## Verify
- [ ] The deployed Cloud Run revision uses the image tag or digest the build pushed.
- [ ] PR builds show plan output and never apply.

## Checked

2026-10-27. Confirmed in the Cloud Build Cloud Run and GKE deploy pages, the user-specified service account page and the Terraform GitOps tutorial: `gke-deploy` flags (`--filename`, `--image`, `--location`, `--cluster`) and its behaviour (digest substitution, wait for readiness), Cloud Run Admin and Service Account User roles, default Cloud Build service account breadth, logging bucket rules with user-specified service accounts, Terraform plan/apply conditional on branch with state in Cloud Storage. Removed: the digest lookup command, `run.developer`, `artifactregistry.writer`, `logging.logWriter`, `container.developer`, Terraform image version and `-lock-timeout`, private-cluster advice, state versioning remark, `$$` escape claim. Read end to end.

Method: documentation only; no commands were run.
