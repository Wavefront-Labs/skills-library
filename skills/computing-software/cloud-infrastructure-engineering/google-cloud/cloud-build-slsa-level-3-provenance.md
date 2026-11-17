---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-slsa-level-3-provenance
name: cloud-build-slsa-level-3-provenance
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, cloud-build-slsa-level3, slsa-level-3, build-provenance, private-pools]
level: advanced
status: docs-checked
description: "Produce SLSA level 3 provenance with Cloud Build: requestedVerifyOption VERIFIED, images and artifacts in Artifact Registry, and viewing provenance."
sources: ["https://cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance", "https://cloud.google.com/build/docs/securing-builds/view-build-security-insights", "https://slsa.dev/spec/v1.0/levels", "https://cloud.google.com/binary-authorization/docs/gke-policy-based/slsa-check"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Build SLSA level 3 provenance

Cloud Build supports generating build provenance that meets SLSA level 3 assurance, based on SLSA specifications 0.1 and 1.0. It only generates provenance for artifacts stored in Artifact Registry.

## 1. Build config
```yaml
steps:
- name: gcr.io/cloud-builders/docker
  args: [build, -t, europe-docker.pkg.dev/$PROJECT_ID/apps/api:$SHORT_SHA, .]
images: [europe-docker.pkg.dev/$PROJECT_ID/apps/api:$SHORT_SHA]   # images pushed by Cloud Build
artifacts:
  goModules: []          # the artifacts block also takes mavenArtifacts, pythonPackages, npmPackages
options:
  requestedVerifyOption: VERIFIED
  logging: CLOUD_LOGGING_ONLY
```
Check the provenance page for which artifact types and push methods are covered before relying on it.

## 2. View
```bash
gcloud artifacts docker images describe europe-docker.pkg.dev/<P>/apps/api@sha256:<D> \
  --show-provenance --format=json | jq '.provenance_summary'
```

## Verify
- [ ] `--show-provenance` returns provenance for the image digest with the build's source and builder details.

## Checked

2026-10-27. Confirmed in the generate-and-validate build provenance page, the cloudbuild v1 discovery schemas (BuildOptions `requestedVerifyOption` enum NOT_VERIFIED, VERIFIED, BEST_EFFORT; Artifacts fields `images`, `goModules`, `mavenArtifacts`, `pythonPackages`, `npmPackages`) and the `gcloud artifacts docker images describe` reference (`--show-provenance`): SLSA level 3 assurance for specs 0.1 and 1.0, provenance only for Artifact Registry artifacts. Removed: `slsa-verifier` command and builder id, Binary Authorization `slsaCheck` (page 404), Security insights console claim (page 404), the no-provenance-for-docker-push claim, and the private pool, manual-build and re-tagging gotchas. Read end to end.

Method: documentation only; no commands were run.
