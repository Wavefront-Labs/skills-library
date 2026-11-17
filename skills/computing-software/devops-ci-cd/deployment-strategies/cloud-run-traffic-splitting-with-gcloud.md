---
id: computing-software.devops-ci-cd.deployment-strategies.cloud-run-traffic-splitting-with-gcloud
name: cloud-run-traffic-splitting-with-gcloud
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, traffic-splitting-gcloud, cloud-run, revision-tags, gcloud-run, gradual-rollout, no-traffic]
level: practitioner
status: draft
description: "Split traffic between Cloud Run revisions with gcloud: --no-traffic deploys, revision tags for test URLs, percentage splits, update-traffic, and automating gradual rollouts."
sources:
  - https://cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration
  - https://cloud.google.com/sdk/gcloud/reference/run/services/update-traffic
  - https://cloud.google.com/deploy/docs/deployment-strategies/canary
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Cloud Run traffic splitting with gcloud

## Deploy without traffic, test via tag
```bash
gcloud run deploy api --image europe-docker.pkg.dev/proj/repo/api@sha256:abc \
  --region europe-west2 --no-traffic --tag candidate
# test URL: https://candidate---api-<hash>-nw.a.run.app
curl -fsS https://candidate---api-xxxx-nw.a.run.app/health
```
`--no-traffic` only works once the service already exists; the first deploy always takes 100%.

## Shift gradually
```bash
gcloud run services update-traffic api --region europe-west2 --to-tags candidate=10
gcloud run services update-traffic api --to-tags candidate=50
gcloud run services update-traffic api --to-latest          # 100% to newest revision and follow future deploys
gcloud run services describe api --format='yaml(status.traffic)'
```
Or by revision name: `--to-revisions api-00042-abc=10,api-00041-xyz=90`. Percentages must sum to 100 when listing all.

## Roll back
```bash
gcloud run services update-traffic api --to-revisions api-00041-xyz=100
```
Pin explicit revisions in production: if traffic is set to "latest", the next deploy goes to 100% immediately.

## Automating
```bash
for pct in 5 25 50 100; do
  gcloud run services update-traffic api --region "$R" --to-tags candidate=$pct
  sleep 600
  err=$(gcloud monitoring time-series list ... )   # or query Cloud Monitoring / your APM for 5xx ratio by revision
  [ "$(echo "$err > 0.01" | bc)" = 1 ] && { gcloud run services update-traffic api --to-revisions "$STABLE"=100; exit 1; }
done
```
Managed alternative: Cloud Deploy with `strategy: canary: runtimeConfig: cloudRun: automaticTrafficControl: true` and `canaryDeployment: percentages: [10, 50]`, with verification jobs between phases.

## Details
- Metrics in Cloud Monitoring carry `revision_name`, so compare error rate and latency per revision.
- Tags are permanent URLs until removed: `--remove-tags candidate`; tagged revisions don't scale to zero cost-free if hit by probes.
- Minimum instances are per revision; a canary at 5% with `min-instances=3` still bills 3 instances.
- Sessions aren't sticky by default; enable `--session-affinity` if users must stay on one revision.
- Terraform: `traffic {}` blocks in `google_cloud_run_v2_service`; ignore changes to traffic if gcloud manages rollouts, or Terraform will revert splits.

## Verify
- [ ] `status.traffic` shows the intended split; revision metrics show the canary receiving its share.
- [ ] Rollback command restores 100% to the previous revision in seconds.
