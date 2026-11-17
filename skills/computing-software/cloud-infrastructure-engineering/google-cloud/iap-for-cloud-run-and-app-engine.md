---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iap-for-cloud-run-and-app-engine
name: iap-for-cloud-run-and-app-engine
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, identity-aware-proxy, iap-cloud-run, iap-app-engine, cloud-run, app-engine, serverless-neg, zero-trust]
level: practitioner
status: docs-checked
description: "Put Identity-Aware Proxy in front of Cloud Run (direct or via a serverless NEG load balancer) and App Engine, grant httpsResourceAccessor, and close every bypass path."
sources: ["https://cloud.google.com/iap/docs/enabling-cloud-run", "https://cloud.google.com/iap/docs/app-engine-quickstart", "https://cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run", "https://cloud.google.com/sdk/gcloud/reference/iap/web"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAP for Cloud Run and App Engine

## Option A — Cloud Run, IAP enabled directly on the service
Simplest; no load balancer.
```bash
gcloud run deploy internal-tool --image=<IMG> --region=<R> --no-allow-unauthenticated --iap
# existing service:
gcloud run services update internal-tool --region=<R> --iap
# IAP's service agent must be able to invoke the service
PN=$(gcloud projects describe <P> --format='value(projectNumber)')
gcloud run services add-iam-policy-binding internal-tool --region=<R> \
  --member=serviceAccount:service-$PN@gcp-sa-iap.iam.gserviceaccount.com --role=roles/run.invoker
# who may use the app
gcloud iap web add-iam-policy-binding --resource-type=cloud-run --service=internal-tool --region=<R> \
  --member=group:tool-users@example.com --role=roles/iap.httpsResourceAccessor
```

## Option B — Cloud Run behind an external Application Load Balancer
Use when you also need Cloud Armor, CDN, a custom domain on one IP, or several services.
1. Serverless NEG → backend service → URL map → HTTPS proxy with a managed cert.
2. `gcloud compute backend-services update <BACKEND_SERVICE> --global --iap=enabled` (use `--region <REGION>` instead of `--global` for a regional backend service).
3. Grant the IAP service agent `roles/run.invoker` as above.
4. **Close the bypass**: `gcloud run services update internal-tool --ingress=internal-and-cloud-load-balancing`
   so the `*.run.app` URL no longer accepts internet traffic.

## App Engine
```bash
gcloud iap web enable --resource-type=app-engine
gcloud iap web add-iam-policy-binding --resource-type=app-engine \
  --member=group:tool-users@example.com --role=roles/iap.httpsResourceAccessor
```
`--service=<APP_ENGINE_SERVICE>` narrows the binding to one App Engine service (the flag exists on `iap web add-iam-policy-binding`).

## Gotchas
- IAP on a load balancer does not protect traffic that reaches the Cloud Run service through its `run.app` URL (Google's guide); restrict ingress, or enable IAP directly on the service.
- With IAP in front of Cloud Run, IAP authenticates to the service using the `X-Serverless-Authorization` header, which Cloud Run strips of its signature before your code sees it.
- The app must still validate `x-goog-iap-jwt-assertion` if any path could bypass IAP.

## Verify
- [ ] An incognito request to the app redirects to Google sign-in; a non-member gets 403 "You don't have access".
- [ ] `curl https://<service>-<hash>.a.run.app` returns 403/404 when fronted by the LB.
- [ ] `gcloud iap web get-iam-policy --resource-type=...` lists only groups.

## Checked

- Date: 2026-10-27
- Confirmed against the Cloud Run IAP page and the *Enable IAP for Cloud Run* guide (`gcloud run deploy ... --no-allow-unauthenticated --iap`, `gcloud run services update --iap`, `service-PROJECT_NUMBER@gcp-sa-iap.iam.gserviceaccount.com` with `roles/run.invoker`, `gcloud compute backend-services update --iap=enabled` global and regional forms, run.app bypass note, `X-Serverless-Authorization`), gcloud references for `run services update --ingress` (default all; value `internal-and-cloud-load-balancing`), `iap web enable` (`--resource-type=app-engine|backend-services`), `iap web add-iam-policy-binding` (`--resource-type`, `--region` required for cloud-run, `--service`) and the IAP signed-headers guide.
- Replaced `iap web enable` for load balancer backends with the documented `compute backend-services update --iap=enabled`. Removed: App Engine cron/task-queue header exemption, whole-app coverage claim, Google-managed OAuth client limitation and the programmatic audience note.

Method: documentation only; no commands were run.
