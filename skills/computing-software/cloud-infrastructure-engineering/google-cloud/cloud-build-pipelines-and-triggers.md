---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-pipelines-and-triggers
name: cloud-build-pipelines-and-triggers
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-build, cloudbuild, cloudbuild-yaml, build-triggers, private-pools, worker-pools, build-service-account, kaniko, buildpacks, build-substitutions, build-approvals, github-connection, developer-connect, build-caching, build-logs, build-provenance, ci-pipeline, repository-connections]
level: practitioner
status: docs-checked
description: "Run CI on Cloud Build: cloudbuild.yaml steps and substitutions, triggers, per-trigger service accounts, private pools in your VPC, and approvals."
sources: ["https://cloud.google.com/build/docs/overview", "https://cloud.google.com/build/docs/build-config-file-schema", "https://cloud.google.com/build/docs/triggers", "https://cloud.google.com/build/docs/private-pools/private-pools-overview", "https://cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts", "https://cloud.google.com/build/docs/optimize-builds/speeding-up-builds", "https://cloud.google.com/build/docs/securing-builds/gate-builds-on-approval"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cloud Build pipelines and triggers

**Goal:** every merge builds an image inside your network with a least-privilege
identity, quickly, and production builds wait for a human approval.

## 1. cloudbuild.yaml that holds up
```yaml
steps:
- id: test
  name: python:3.12-slim
  entrypoint: bash
  args: ['-c', 'pip install -r requirements.txt && pytest -q']
- id: build
  name: gcr.io/cloud-builders/docker
  args: [build, -t, '${_REGION}-docker.pkg.dev/${PROJECT_ID}/img/app:${SHORT_SHA}', .]
  waitFor: ['test']
images: ['${_REGION}-docker.pkg.dev/${PROJECT_ID}/img/app:${SHORT_SHA}']
substitutions: {_REGION: europe-west1}
options:
  logging: CLOUD_LOGGING_ONLY
  machineType: E2_HIGHCPU_8
  dynamicSubstitutions: true
  requestedVerifyOption: VERIFIED          # SLSA provenance
  pool: {name: "projects/${PROJECT_ID}/locations/europe-west1/workerPools/private"}
timeout: 1200s
serviceAccount: projects/${PROJECT_ID}/serviceAccounts/cb-app@${PROJECT_ID}.iam.gserviceaccount.com
```
- Steps run sequentially unless `waitFor` says otherwise (`waitFor: ['-']` starts a step immediately). `images:` plus `requestedVerifyOption: VERIFIED` yields provenance (see `cloud-build-slsa-level-3-provenance`).
- Built-in substitutions include `PROJECT_ID`, `PROJECT_NUMBER`, `BUILD_ID`, `COMMIT_SHA`, `SHORT_SHA`, `REPO_NAME`, `BRANCH_NAME`, `TAG_NAME`, `TRIGGER_NAME`; user substitutions start with `_` and can be overridden per trigger.
- `logging: CLOUD_LOGGING_ONLY` stores build logs in Cloud Logging; with a user-specified service account, logs must go to a user-owned Cloud Storage bucket or a Cloud Logging bucket.
- `timeout` defaults to 60 minutes (maximum 24 hours). `machineType` values are listed in `cloud-build-timeouts-machine-types-and-concurrency`.

## 2. Triggers and repo connections
```bash
gcloud builds connections create github gh-conn --region=europe-west1
gcloud builds repositories create app --connection=gh-conn --region=europe-west1 --remote-uri=https://github.com/example/app.git
gcloud builds triggers create github --name=app-main --region=europe-west1 \
  --repository=projects/P/locations/europe-west1/connections/gh-conn/repositories/app \
  --branch-pattern='^main$' --build-config=cloudbuild.yaml --service-account=projects/P/serviceAccounts/cb-app@P.iam.gserviceaccount.com \
  --substitutions=_REGION=europe-west1 --include-logs-with-status
gcloud builds triggers create github --name=app-pr ... --pull-request-pattern='.*' --comment-control=COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY
```
- Triggers respond to repository events such as pushes and pull requests; `--included-files` limits a trigger to given paths.
- **Approvals**: a trigger with `--require-approval` leaves the build pending until a user with the Cloud Build Approver role approves it; pending builds older than 2 months cannot be approved or rejected. Pair with a production trigger on tags only.
- `--region` on triggers and connections keeps them regional.

## 3. Identity (stop using the default SA)
- Without a user-managed service account Cloud Build uses the default Cloud Build service account, which may have unnecessarily broad permissions (for example access to Cloud Source Repositories and every Cloud Storage bucket in the project).
- Create a service account per task (for example one that builds and pushes images to Artifact Registry) and grant it only the roles that task needs; set `--service-account` on every trigger.

## 4. Private pools (build inside the VPC)
```bash
gcloud builds worker-pools create private --region=europe-west1 --peered-network=projects/<HOST>/global/networks/prod-vpc \
  --worker-machine-type=<MACHINE_TYPE> --worker-disk-size=<GB> --no-public-egress
```
Private pools can peer into a VPC or shared VPC to reach private resources, support VPC Service Controls, and allow larger machine types and disks than the default pool. See the private pools overview for networking prerequisites and pricing.

## 5. Faster builds
- Cache: `--cache-from` with a previously pushed image speeds Docker builds.
- Bigger `machineType`, parallel steps with `waitFor`, per-step and per-build `timeout`.
- Quotas on concurrent builds and CPUs apply per region (see the Cloud Build quotas page).

## Gotchas
- PR triggers: `--comment-control` decides whether builds wait for a `/gcbrun` comment from a user with repository write permission; use `COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY` or `COMMENTS_ENABLED` on repositories that accept outside contributions.
- Pin builder images by digest rather than `latest` so builds are reproducible.

## Verify
- [ ] Push to `main` builds, pushes `app:<sha>` and `gcloud artifacts docker images describe <IMAGE>@sha256:<D> --show-provenance` returns provenance.
- [ ] A PR from a fork does not auto-run the build without a maintainer comment.
- [ ] A build on the private pool uses no public egress when `--no-public-egress` is set.
- [ ] The production trigger's build stays pending until an approver approves it.

## Checked

2026-10-27. Confirmed in the build config schema, triggers, approval, substitutions, private pools overview and user-specified service account pages, the cloudbuild v1 discovery schemas (BuildOptions enums and fields, Build timeout default 60 minutes, maximum stated on the schema page as 24 hours, PullRequestFilter commentControl enum) and the `gcloud builds` reference pages (connections create github, repositories create, triggers create github, worker-pools create: every flag in the examples exists). Removed: Kaniko flags and the Kaniko, buildpacks and `latest` image claims, the vulnerability-scan and Cloud Deploy release steps, the NPM_TOKEN secret example, the IAM role list, legacy and Compute default service account claims, metric names, `gcloud builds approve` (reference page 404), cache-in-GCS advice, Artifact Registry region and logging gotchas, build-duration and `curl ifconfig.me` checks, pricing remarks. Read end to end.

Method: documentation only; no commands were run.
