---
id: computing-software.cloud-infrastructure-engineering.google-cloud.troubleshooting-function-build-and-deploy-failures
name: troubleshooting-function-build-and-deploy-failures
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-run-functions, function-build-failures, function-deploy-errors, cloud-build-logs, buildpacks, artifact-registry]
level: practitioner
status: docs-checked
description: "Fix Cloud Run functions deploy failures: Cloud Build logs, build service account permissions, entry-point and region errors, actAs, VPC connector roles, container start failures."
sources: ["https://cloud.google.com/functions/docs/troubleshooting", "https://cloud.google.com/functions/docs/securing/build-custom-sa", "https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting function build and deploy failures

Deploy = upload source -> **Cloud Build** with Google buildpacks -> image in Artifact Registry
(`gcf-artifacts` repo) -> Cloud Run revision. Find which stage failed.

## Get the build log
```bash
gcloud functions deploy fn ...                           # prints the build log URL on failure
gcloud builds list --region=<R> --limit=5
gcloud builds log <BUILD_ID> --region=<R>
```

## Build-stage errors
| Message | Fix |
|---|---|
| `Could not build the function due to a missing permission on the build service account` | the build SA must read the source bucket and read/write the Artifact repository; it can also follow an org policy change or Cloud Build's default service account change. Create a custom build SA (`--build-service-account`) or add `roles/cloudbuild.builds.builder` to the default Compute SA |
| build service account disabled | the build SA must be enabled to deploy; create a custom build SA for function deployments |
| entry point not found | the source must contain an entry point function and the deployment (console or `gcloud`) must name it correctly |
| `"LOCATION" violates constraint "constraints/gcp.resourceLocations"` (400) | the org policy does not allow the function's location; pick an allowed region |

Images are stored in `REGION-docker.pkg.dev/PROJECT_ID/gcf-artifacts` in the function's project. A custom
build SA typically needs `roles/logging.logWriter`, `roles/artifactregistry.writer` (on `gcf-artifacts` and
`cloud-run-source-deploy`) and `roles/storage.objectViewer`.

## Deploy-stage errors
- `The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable`: read the revision logs and check the entry point is specified correctly.
- `Caller is missing permission 'iam.serviceaccounts.actAs'` (403): grant the deployer `roles/iam.serviceAccountUser` on the runtime service account.
- VPC connector in a bad state: `PROJECT_NUMBER@cloudservices.gserviceaccount.com` and `service-PROJECT_NUMBER@gcp-sa-vpcaccess.iam.gserviceaccount.com` must not be missing permissions; in Shared VPC they need `roles/compute.networkUser` in the host project.

## Gotchas
- Build environment variables use `--set-build-env-vars`, not runtime env vars.

## Verify
- [ ] Clean deploy succeeds and first request returns 200 with no startup errors in logs.

## Checked
2026-10-31. Confirmed against the Cloud Run functions troubleshooting page and the build service account page: `gcf-artifacts` repository, build service account errors and fixes, `gcp.resourceLocations` error, PORT=8080 startup error, actAs error and role, VPC connector service accounts and roles, build SA roles. Removed: Python/npm dependency and handler messages, private-repository, Cloud Build quota rows, the `tags` build filter, `.gcloudignore` and the "no longer gets Editor" claim.
Method: documentation only; no commands were run.
