---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-deploy-delivery-pipelines
name: cloud-deploy-delivery-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-deploy, delivery-pipeline, deployment-strategies, canary, blue-green, progressive-delivery, skaffold, releases, rollouts, promotion, approvals, deploy-hooks, verify-phase, automation-rules, gke-deploy, cloud-run-deploy, custom-targets, rollback, deploy-policies]
level: practitioner
status: docs-checked
description: "Continuous delivery with Cloud Deploy: pipelines and targets for GKE and Cloud Run, canary with verify, approvals, automations, rollback and deploy policies."
sources: ["https://docs.cloud.google.com/deploy/docs/overview", "https://docs.cloud.google.com/deploy/docs/create-pipeline-targets", "https://docs.cloud.google.com/deploy/docs/deployment-strategies/canary", "https://docs.cloud.google.com/deploy/docs/verify-deployment", "https://docs.cloud.google.com/deploy/docs/automation", "https://docs.cloud.google.com/deploy/docs/deploy-policy", "https://docs.cloud.google.com/deploy/docs/roll-back", "https://clouddeploy.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Deploy delivery pipelines

**Goal:** one release promoted dev, staging, prod with the same rendered manifests, a canary that verifies itself, humans approving only where policy says so, and rollback that is one command.

## 1. Pipeline and targets
```yaml
# clouddeploy.yaml
apiVersion: deploy.cloud.google.com/v1
kind: DeliveryPipeline
metadata: {name: app}
serialPipeline:
  stages:
  - targetId: dev
    profiles: [dev]
  - targetId: staging
    profiles: [staging]
    strategy: {standard: {verify: true}}
  - targetId: prod
    profiles: [prod]
    strategy:
      canary:
        runtimeConfig: {kubernetes: {gatewayServiceMesh: {httpRoute: app-route, service: app, deployment: app}}}   # or serviceNetworking for GKE, or cloudRun: {automaticTrafficControl: true}
        canaryDeployment: {percentages: [10, 50], verify: true}
    deployParameters: [{values: {replicaCount: "6"}}]
---
apiVersion: deploy.cloud.google.com/v1
kind: Target
metadata: {name: prod}
requireApproval: true
gke: {cluster: projects/P/locations/europe-west1/clusters/prod, internalIp: true}
executionConfigs:
- usages: [RENDER, DEPLOY, VERIFY]
  workerPool: projects/P/locations/europe-west1/workerPools/private
  serviceAccount: cd-prod@P.iam.gserviceaccount.com
  executionTimeout: 1800s
```
`gcloud deploy apply --file=clouddeploy.yaml --region=europe-west1`. A target is one of `gke`, `run` (`run: {location: projects/P/locations/europe-west1}`), `anthosCluster`, `multiTarget` (several child targets deployed in parallel) or `customTarget`. `internalIp: true` reaches the GKE control plane by its private IP; `workerPool` is a Cloud Build private pool; `executionTimeout` must be between 10 minutes and 24 hours.

## 2. Skaffold does render and deploy
Each stage's `profiles` selects a Skaffold profile from `skaffold.yaml`, which defines the manifests (kustomize, Helm and so on) and optional `verify` containers; see the Skaffold documentation for that file. Cloud Deploy renders the manifests for every target when you create the release, so what rendered is what is deployed:
```bash
gcloud deploy releases create rel-$SHA --delivery-pipeline=app --region=europe-west1 \
  --images=app=europe-docker.pkg.dev/P/img/app@sha256:<DIGEST>
```
`deployParameters` are substituted after rendering. Pin Skaffold per release with the release's `skaffoldVersion` field (the `--skaffold-version` flag on `releases create`), not in the target.

## 3. Rollout flow
- `releases create` creates a rollout to the first stage. `gcloud deploy releases promote --release=rel-... --to-target=staging` creates a rollout on the next (or named) target. Targets with `requireApproval` wait in `PENDING_APPROVAL` until `gcloud deploy rollouts approve`.
- **Canary** phases are `canary-<percent>` for each percentage plus a final `stable` phase, advanced with `rollouts advance` or by an `advanceRolloutRule` automation. The Gateway API configuration allows 100%; GKE service-based, attached clusters and Cloud Run do not. Canary supports GKE (service networking or Gateway API), attached clusters and Cloud Run services and worker pools (not jobs).
- **Verify**: after deployment Cloud Deploy runs your test containers in its execution environment. Exit code 0 is success, non-zero is failure; a failed verification fails the rollout. You can ignore or retry a failed verification and terminate an in-progress verify job.
- **Deploy hooks**: `predeploy` and `postdeploy` jobs can be added to a strategy; analysis jobs can gate canary phases.
- **Automations** (`kind: Automation`): `promoteReleaseRule` (promote on success, optional `wait`), `advanceRolloutRule`, `repairRolloutRule` (retry a set number of times, then roll back) and `timedPromoteReleaseRule` (crontab `schedule` plus IANA `timeZone`).
- **Rollback**: `gcloud deploy targets rollback prod --delivery-pipeline=app` creates a new rollout from the last release with a successful rollout to that target; `--release` picks another. For an older release use `releases promote` with `--to-target`.
- **Deploy policies** (`kind: DeployPolicy`): a `rolloutRestriction` with `timeWindows`, optional `invokers` (`USER`, `DEPLOY_AUTOMATION`) and `actions` (`ADVANCE`, `APPROVE`, `CANCEL`, `CREATE`, `IGNORE_JOB`, `RETRY_JOB`, `ROLLBACK`, `TERMINATE_JOBRUN`; empty means all). Override one with `--override-deploy-policies=<POLICY>` if you hold `clouddeploy.deployPolicies.override` (role `roles/clouddeploy.policyOverrider`).

## 4. IAM and notifications
- `roles/clouddeploy.releaser` creates releases and rollouts; `roles/clouddeploy.approver` approves or rejects rollouts; `roles/clouddeploy.viewer` is read-only; `roles/clouddeploy.jobRunner` lets an execution service account write logs and Cloud Storage objects without delivering to a target. Users with the admin, developer or operator role need `iam.serviceAccounts.actAs` on a target's alternate service account.
- Pub/Sub topics `clouddeploy-resources`, `clouddeploy-operations`, `clouddeploy-approvals` and `clouddeploy-advances` must be created (same names) before Cloud Deploy publishes to them.

## Gotchas
- Canary on GKE needs a routing mechanism: Gateway API or service networking.
- `executionConfigs` default to the default Cloud Build pool and, when `serviceAccount` is unset, the project's default compute service account; set both when you need private pools or tighter permissions.
- Release rendering state is `renderState` (`SUCCEEDED`, `FAILED`, `IN_PROGRESS`).
- Keep `clouddeploy.yaml` in the same repo and `apply` it before `releases create`.

## Verify
- [ ] `gcloud deploy releases describe` shows `renderState: SUCCEEDED` for the release and the dev rollout succeeds.
- [ ] A failing staging verify container fails the rollout.
- [ ] A promote during the freeze window is refused by the deploy policy unless overridden.

## Checked
2026-10-28. Confirmed against the Cloud Deploy overview, canary, verify, rollback, automation (rule names), deploy-policy and notifications pages, the IAM roles page, and the Cloud Deploy v1 discovery document (`Strategy`, `Canary`, `KubernetesConfig`, `GatewayServiceMesh`, `GkeCluster.internalIp`, `ExecutionConfig`, `AutomationRule`, `PromoteReleaseRule.wait`, `TimedPromoteReleaseRule`, `RolloutRestriction`, `Release.skaffoldVersion` and `renderState`). Corrected: `skaffoldVersion` belongs to the release, not the target; render state is `SUCCEEDED`, not `RENDERED`; deploy-policy `actions` are the listed enum values. Removed: the Skaffold YAML sample, the staging-bucket and SLSA security-insights claims, the "private chart repos" note, the sub-two-minute rollback target and the 10 percent traffic check.
Method: documentation only; no commands were run.
