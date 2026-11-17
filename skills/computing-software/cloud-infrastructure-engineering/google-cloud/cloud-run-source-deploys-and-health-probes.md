---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-run-source-deploys-and-health-probes
name: cloud-run-source-deploys-and-health-probes
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run, cloud-run-deploy-from-source, gcloud-run-deploy, cloud-run-health-checks, startup-probe, liveness-probe, buildpacks]
level: practitioner
status: docs-checked
description: "Deploy Cloud Run services from source or images with gcloud run deploy, configure startup and liveness probes and CPU boost, and roll out revisions without serving broken ones."
sources: ["https://docs.cloud.google.com/run/docs/deploying-source-code", "https://docs.cloud.google.com/run/docs/configuring/healthchecks", "https://docs.cloud.google.com/run/docs/configuring/services/build-service-account", "https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration", "https://docs.cloud.google.com/run/docs/configuring/cpu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Run source deploys and health probes

## 1. Deploy from source
```bash
gcloud run deploy orders --source=. --region=europe-west2 \
  --service-account=orders-run@<P>.iam.gserviceaccount.com \
  --no-allow-unauthenticated --cpu-boost --set-env-vars=APP_ENV=prod
```
With a `Dockerfile` it builds that; otherwise Google Cloud buildpacks detect the language. The
image goes to an Artifact Registry repository named `cloud-run-source-deploy`, created automatically in the region if it does not exist. In CI prefer building once and
`gcloud run deploy --image=<AR_IMAGE>@sha256:...` so every environment runs the same digest.

## 2. Probes
```bash
gcloud run deploy orders --image=<IMG> --region=<R> \
  --startup-probe=httpGet.path=/healthz/ready,httpGet.port=8080,initialDelaySeconds=0,periodSeconds=2,failureThreshold=60,timeoutSeconds=1 \
  --liveness-probe=httpGet.path=/healthz/live,periodSeconds=10,failureThreshold=3,timeoutSeconds=2
```
YAML equivalent under `spec.template.spec.containers[0]`: `startupProbe:` / `livenessProbe:` with
`httpGet`, `tcpSocket` or `grpc`.
- With no startup probe, Cloud Run configures a TCP startup probe with `timeoutSeconds: 240`, `periodSeconds: 240` and `failureThreshold: 1`.
- The startup window (`failureThreshold` x `periodSeconds`) cannot exceed 600 seconds (1800 for GPU); slow model/JIT loads need `--cpu-boost` and a generous threshold.
- `timeoutSeconds` cannot exceed `periodSeconds`. Liveness probes support HTTP and gRPC only and start after the startup probe succeeds.
- Liveness failure kills the container with SIGKILL (in-flight requests get 503) and autoscaling starts a new instance; keep the endpoint cheap and independent of downstreams (don't fail liveness because the DB is down).

## 3. Safe rollout
```bash
gcloud run deploy orders --image=<IMG> --region=<R> --no-traffic --tag=canary
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://canary---orders-<hash>.a.run.app/healthz/ready
gcloud run services update-traffic orders --region=<R> --to-tags=canary=10
gcloud run services update-traffic orders --region=<R> --to-latest     # or --to-revisions=<OLD>=100 to roll back
```

## Gotchas
- Read the container logs when a deploy fails its health check, not just the deploy error.
- Source deploys build as the Compute Engine default service account unless you pass `--build-service-account`; that account needs `roles/run.builder` on the project. The deployer needs `roles/run.sourceDeveloper`, `roles/serviceusage.serviceUsageConsumer` and `roles/iam.serviceAccountUser` on the service identity.
- Enforcing the `iam.automaticIamGrantsForDefaultServiceAccounts` constraint means default service accounts no longer get Editor automatically, so grant their roles yourself.

## Verify
- [ ] `gcloud run revisions describe <REV> --region=<R>` shows the startup and liveness probes you configured.

## Checked

2026-10-24, Cloud Run source deploy, health check, build service account, rollout/traffic and CPU pages on docs.cloud.google.com. Confirmed: `cloud-run-source-deploy` repository, Dockerfile versus buildpacks, `--build-service-account`, `roles/run.builder` and deployer roles, probe flag grammar and field names, default TCP startup probe values, 600 s (1800 s GPU) startup-window limit, liveness behaviour, `--no-traffic --tag`, `update-traffic --to-tags/--to-latest/--to-revisions`, tagged URL format, `--cpu-boost`. Corrected: startup-window cap was stated as 240 s. Removed unconfirmed `.gcloudignore` and min/max-instance claims.

Method: documentation only; no commands were run.
