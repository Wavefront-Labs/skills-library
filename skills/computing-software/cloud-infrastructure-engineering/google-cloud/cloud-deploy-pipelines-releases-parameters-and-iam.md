---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-deploy-pipelines-releases-parameters-and-iam
name: cloud-deploy-pipelines-releases-parameters-and-iam
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-deploy, clouddeploy-yaml, pipeline-yaml, gcloud-deploy-releases, deploy-parameters, cloud-deploy-notifications, cloud-deploy-iam, deploy-roles, canary]
level: advanced
status: docs-checked
description: "Set up Cloud Deploy: pipeline and target YAML with canary, releases and promotion with gcloud, deploy parameters, Pub/Sub notifications and least-privilege IAM."
sources: ["https://docs.cloud.google.com/deploy/docs/config-files", "https://docs.cloud.google.com/deploy/docs/overview", "https://docs.cloud.google.com/deploy/docs/parameters", "https://docs.cloud.google.com/deploy/docs/subscribe-deploy-notifications", "https://docs.cloud.google.com/deploy/docs/iam-roles-permissions", "https://clouddeploy.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Deploy: pipelines, releases, parameters and IAM

## 1. Pipeline and targets
```yaml
# clouddeploy.yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata: {name: web}
serialPipeline:
  stages:
  - targetId: staging
    profiles: [staging]
  - targetId: prod
    profiles: [prod]
    strategy:
      canary:
        runtimeConfig: {cloudRun: {automaticTrafficControl: true}}
        canaryDeployment: {percentages: [10, 50], verify: true}
    deployParameters:
    - values: {minInstances: "3"}
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata: {name: prod}
requireApproval: true
run: {location: projects/<P>/locations/europe-west2}
executionConfigs:
- usages: [RENDER, DEPLOY, VERIFY]
  serviceAccount: deploy-exec-prod@<P>.iam.gserviceaccount.com
```
```bash
gcloud deploy apply --file=clouddeploy.yaml --region=europe-west2 --project=<P>
```

## 2. Releases and promotion
```bash
gcloud deploy releases create web-${SHORT_SHA} --delivery-pipeline=web --region=europe-west2 \
  --images=web=europe-west2-docker.pkg.dev/<P>/apps/web@sha256:<DIGEST> \
  --skaffold-file=skaffold.yaml --deploy-parameters=logLevel=info
gcloud deploy releases promote --release=web-${SHORT_SHA} --delivery-pipeline=web --region=europe-west2
gcloud deploy rollouts approve <ROLLOUT> --release=web-${SHORT_SHA} --delivery-pipeline=web --region=europe-west2
gcloud deploy targets rollback prod --delivery-pipeline=web --region=europe-west2
```
Creating a release renders the manifest for each target; the first `releases create` also creates a rollout to the first target. `releases promote` creates a rollout on the next target (or `--to-target`).

## 3. Deploy parameters
In manifests, mark fields: `minScale: 1 # from-param: ${minInstances}`. Values come from
release (`--deploy-parameters`), pipeline stage, or target `deployParameters`. Substitution happens after rendering; the placeholder syntax is `PROPERTY: DEFAULT # from-param: ${KEY}` and the default is required (it may be empty). If one key gets different values in more than one place, `releases create` fails.

## 4. Notifications
Create Pub/Sub topics with these exact names (and enable the Cloud Deploy and Pub/Sub APIs); Cloud Deploy publishes to them:
`clouddeploy-resources` (create/update/delete of core resources), `clouddeploy-operations` (render and deploy events), `clouddeploy-approvals` (approval needed, approved or rejected) and `clouddeploy-advances` (phase advanced or ready to advance). Use push or pull subscriptions, for example a function that posts approvals to chat.

## 5. IAM
| Who | Role |
|---|---|
| CI that creates releases | `roles/clouddeploy.releaser` (create releases and rollouts; no approve) |
| Approvers (humans) | `roles/clouddeploy.approver` (conditioned to prod target if needed) |
| Execution SA | `roles/clouddeploy.jobRunner` (log entries and Cloud Storage objects; no delivery to targets), plus whatever the target runtime needs to deploy |
| Viewers | `roles/clouddeploy.viewer` |
Separate execution SAs per environment so staging can't deploy prod. When a target names an alternate service account, users with the admin, developer or operator roles also need `iam.serviceAccounts.actAs` on it. Do not grant `roles/clouddeploy.serviceAgent` to anyone but the service agent.

## Gotchas
- `requireApproval: true` on a target holds its rollouts until someone with `clouddeploy.approver` approves.
- `executionConfigs` `usages` accept RENDER, DEPLOY, VERIFY, PREDEPLOY, POSTDEPLOY and ANALYSIS; `executionTimeout` must be between 10 minutes and 24 hours. If `serviceAccount` is unset the project's default compute service account is used.
- Give the execution service account only what render, deploy and verify need.

## Verify
- [ ] `gcloud deploy delivery-pipelines describe web --region=<R>` shows both targets; a test release reaches staging and pauses at prod approval.
- [ ] Rollback restores the previous release.

## Checked
2026-10-28. Confirmed against the Cloud Deploy deploy-parameters page (placeholder syntax, required default, failure on differing values), the notifications page (four topic names and what they carry), the IAM roles page (releaser, approver, viewer, jobRunner permissions, actAs note, service-agent warning), the config-files and overview pages, and the Cloud Deploy v1 discovery document (`Canary`, `CanaryDeployment.percentages`/`verify`, `CloudRunConfig.automaticTrafficControl`, `Target.run`/`requireApproval`/`executionConfigs`, `ExecutionConfig.usages`/`executionTimeout`). Removed: the "immutable release" claim, `run.developer`/`container.developer`/`logging.logWriter` grants, silent image-tag substitution, the verify-container description, and the five-minute rollback target.
Method: documentation only; no commands were run.
