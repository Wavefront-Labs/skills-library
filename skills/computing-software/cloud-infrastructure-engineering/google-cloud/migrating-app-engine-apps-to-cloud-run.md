---
id: computing-software.cloud-infrastructure-engineering.google-cloud.migrating-app-engine-apps-to-cloud-run
name: migrating-app-engine-apps-to-cloud-run
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, app-engine, app-engine-to-cloud-run, app2run, legacy-bundled-services, cloud-run-migration, dispatch-rules]
level: practitioner
status: docs-checked
description: "Move App Engine standard or flexible services to Cloud Run: map app.yaml settings, replace legacy bundled services, handle cron, dispatch and domains, and cut over traffic."
sources: ["https://cloud.google.com/appengine/migration-center/run/compare-gae-with-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating App Engine apps to Cloud Run

## Mapping
| App Engine | Cloud Run |
|---|---|
| service/version | service/revision (tagged revision URLs) |
| `instance_class: F2` | `--cpu`/`--memory` |
| `automatic_scaling.max_concurrent_requests` | `--concurrency` |
| `min_instances`/`max_instances` | same flags |
| secrets | Secret Manager, mounted as a volume or passed as environment variables |
| `handlers` static files | Cloud Run has no handlers: serve from the service like dynamic content, or from Cloud Storage |
| `/_ah/warmup` | none needed: Cloud Run warms instances with the container entrypoint; use a startup probe for startup work |

## Legacy bundled services (Python 2/Java 8 era APIs)
Legacy bundled services are available on App Engine (Java, Python, Go and PHP only) but not on Cloud Run, so replace them before or during migration. Second-generation runtimes reach them on App Engine through `app_engine_apis: true` or `app_engine_bundled_services`.

## Deploy
```bash
gcloud run deploy web --source=. --region=<R> --service-account=web@<P>.iam.gserviceaccount.com \
  --cpu=1 --memory=512Mi --concurrency=80 --min-instances=1 --allow-unauthenticated
```
Source deploy uses Google Cloud buildpacks. App Engine's `entrypoint` from app.yaml has no direct equivalent: with `gcloud run deploy --source` you can only configure the entrypoint through a `Procfile`.

## Cutover
1. Put an external ALB in front with both backends (serverless NEGs to App Engine and Cloud Run).
2. Shift paths or weights gradually; move custom domain to the LB.
3. Stop the App Engine versions (`gcloud app versions stop --service=SERVICE VERSION`) once traffic is zero.

## Gotchas
- Request timeouts: App Engine automatic scaling 10 min, basic/manual 24 h; Cloud Run is configurable up to 60 min (default 5 min).
- Health checks are automatic on App Engine; on Cloud Run you define startup and liveness probes yourself.
- Basic-scaling behaviour (scale to zero when idle) maps to Cloud Run min instances of 0.

## Verify
- [ ] All paths served by Cloud Run with parity tests passing; App Engine traffic at zero.

## Checked
2026-10-27. Confirmed against the Compare App Engine and Cloud Run page (instance class mapping, concurrency and min/max instance settings, request timeouts, health checks, warmup requests, static content handlers, Secret Manager, legacy bundled services availability, Procfile-only entrypoint for source deploys) and the App Engine how-instances-are-managed page (versions stop); gcloud run deploy flags. The migrate-to-cloud-run and services/access pages returned 404 and were removed from sources. Removed: cron, dispatch and queue mapping rows, app2run tool, per-service replacement list, default SA row, region and app-deletion claims, GOOGLE_ENTRYPOINT.
Method: documentation only; no commands were run.
