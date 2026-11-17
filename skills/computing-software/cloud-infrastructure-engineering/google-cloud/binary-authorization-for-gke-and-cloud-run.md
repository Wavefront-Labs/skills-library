---
id: computing-software.cloud-infrastructure-engineering.google-cloud.binary-authorization-for-gke-and-cloud-run
name: binary-authorization-for-gke-and-cloud-run
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, binauthz-gke-cloud-run, platform-policy, continuous-validation, org-policy]
level: advanced
status: docs-checked
description: "Turn on Binary Authorization enforcement for GKE clusters and Cloud Run services, use GKE platform policies with continuous validation, and require it with org policy."
sources: ["https://cloud.google.com/binary-authorization/docs/setting-up", "https://cloud.google.com/binary-authorization/docs/run/enabling-binauthz-cloud-run", "https://cloud.google.com/binary-authorization/docs/gke-policy-based/overview", "https://cloud.google.com/binary-authorization/docs/run/requiring-binauthz-cloud-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary Authorization for GKE and Cloud Run

## 1. GKE
```bash
gcloud container clusters update prod --location=<R> \
  --binauthz-evaluation-mode=project-singleton-policy-enforce
```
- `--binauthz-evaluation-mode` accepts `disabled` or `project-singleton-policy-enforce` (admission control by the project policy); `--enable-binauthz` is deprecated.
- Export and import the project policy with `gcloud container binauthz policy export` and `gcloud container binauthz policy import`.
- Platform policies and continuous validation for GKE were not checkable (the policy-based overview and SLSA check pages returned 404): follow the current Binary Authorization documentation for them.

## 2. Cloud Run
```bash
gcloud run services update api --region=<R> --binary-authorization=default
gcloud run deploy api --image=<AR>/api@sha256:<D> --region=<R> --binary-authorization=default
```
Binary Authorization policy-based deployment applies to Cloud Run services and jobs (`gcloud run jobs update JOB --binary-authorization=POLICY`). Attestations (for example the built-by-cloud-build attestor) can limit deploys to images built by Cloud Build or signed by you.

## 3. Require it
Org policy `run.allowedBinaryAuthorizationPolicies` limits which Binary Authorization policies Cloud Run services may use, for example `gcloud resource-manager org-policies allow run.allowedBinaryAuthorizationPolicies default --organization=<ORG_ID>`, so only `default` is permitted.

## Gotchas
- Break-glass deploys (`--breakglass=<JUSTIFICATION>`) bypass policy constraints and are cleared by the next update or deploy; audit their use.

## Verify
- [ ] `gcloud container clusters describe prod --location=<R>` shows Binary Authorization enabled, `gcloud run services describe api` shows the policy, and an unattested deploy is rejected.

## Checked

2026-10-27. Confirmed in the Binary Authorization Cloud Run pages and the `clusters update`, `binauthz policy export` and `gcloud run` reference pages: `--binauthz-evaluation-mode` values `disabled` and `project-singleton-policy-enforce` (lowercase, `--enable-binauthz` deprecated), `gcloud run services update/deploy --binary-authorization=default`, `gcloud run jobs update --binary-authorization`, built-by-cloud-build attestor, `run.allowedBinaryAuthorizationPolicies` with the value `default`. Removed: `--binauthz-policy-bindings`, `POLICY_BINDINGS`, check names (imageFreshnessCheck and others), `gcloud beta container binauthz policy create` (no reference page), the `container.googleapis.com/Cluster` custom-constraint advice, system-image, sidecar and continuous-validation gotchas, digest advice, unconfirmed `--format` projections. Read end to end.

Method: documentation only; no commands were run.
