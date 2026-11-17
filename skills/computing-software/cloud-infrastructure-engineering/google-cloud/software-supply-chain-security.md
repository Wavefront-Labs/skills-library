---
id: computing-software.cloud-infrastructure-engineering.google-cloud.software-supply-chain-security
name: software-supply-chain-security
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, slsa, artifact-analysis, container-scanning, vulnerability-scanning, binary-authorization, attestations, attestors, provenance, cloud-build-provenance, sbom, assured-oss, sigstore, cosign, software-delivery-shield, on-demand-scanning, kritis, continuous-validation, image-signing]
level: advanced
status: docs-checked
description: "Secure the build-to-deploy chain: Artifact Analysis scanning and SBOMs, SLSA provenance from Cloud Build, Binary Authorization attestors and policies, validation, Assured OSS."
sources: ["https://cloud.google.com/software-supply-chain-security/docs/overview", "https://cloud.google.com/artifact-analysis/docs/artifact-analysis", "https://cloud.google.com/build/docs/securing-builds/generate-validate-build-provenance", "https://cloud.google.com/binary-authorization/docs/overview", "https://cloud.google.com/binary-authorization/docs/creating-attestors-cli", "https://cloud.google.com/assured-open-source-software/docs/overview"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Software supply chain security

**Goal:** only images that were built by your pipeline from reviewed source, scanned, and
signed can run in production, and you can prove it for any image hash later.

## 1. Scan what you store (Artifact Analysis)
- Artifact Analysis provides the vulnerability information that Binary Authorization can use to control deployment, and stores the trusted metadata (notes and occurrences) used in authorization. Check the Artifact Analysis pages for current scanning scope and how long images are rescanned.
- The scan commands are `gcloud artifacts docker images scan <IMAGE> --remote` (on-demand) and `gcloud artifacts docker images list-vulnerabilities <IMAGE_OR_SCAN>`; gate CI on the findings your policy cares about.
- SBOMs: `gcloud artifacts sbom export --uri=<IMAGE@DIGEST>` (see the Artifact Analysis SBOM page).

## 2. Provenance from the build (SLSA)
Cloud Build can generate build provenance that meets SLSA level 3 assurance (SLSA spec versions 0.1 and 1.0). The provenance records digests of the built images, source locations, build arguments and duration. To make provenance mandatory, set `options: {requestedVerifyOption: VERIFIED}` in the build config: builds are only marked successful if provenance is generated. View it with `gcloud artifacts docker images describe <LOCATION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE>@sha256:<HASH> --show-provenance`.
The Cloud Build, Cloud Run and GKE consoles show security insights about build artifacts and dependencies.

## 3. Binary Authorization
Binary Authorization enforces that images deployed to GKE, Cloud Run, Cloud Service Mesh or Google Distributed Cloud conform to a policy you define. It is based on the Kritis specification (part of Grafeas). The common use case is **attestations**: an attestation certifies that an image completed a pipeline stage, and the policy verifies it at deploy time.
```bash
# attestor backed by a KMS signing key
gcloud container binauthz attestors create build-attestor --attestation-authority-note=build-note --attestation-authority-note-project=<PROJECT_ID>
gcloud container binauthz attestors public-keys add --attestor=build-attestor \
  --keyversion=projects/<KMS_PROJECT>/locations/global/keyRings/<RING>/cryptoKeys/<KEY>/cryptoKeyVersions/1
# sign in CI after the scan gate
gcloud beta container binauthz attestations sign-and-create --artifact-url=<LOCATION>-docker.pkg.dev/<PROJECT_ID>/<REPOSITORY>/<IMAGE>@sha256:<HASH> \
  --attestor=build-attestor --attestor-project=<PROJECT_ID> --keyversion=...
```
- **Continuous validation (CV)** with check-based platform policies (Preview at the time of checking) periodically checks images of running Pods against a policy and writes log entries to Cloud Logging when they do not conform.
- Start new policies in a non-blocking mode and watch the audit logs before enforcing; see the Binary Authorization policy reference for the current enforcement modes.

## 4. Dependencies: Assured OSS and private mirrors
- **Assured Open Source Software** provides OSS packages built by Google, meeting SLSA level 3 with verifiable provenance and SBOMs (SPDX) plus VEX information (CycloneDX). It covers Java, Go, Python and JavaScript (npm) packages. The Free tier covers Python, Go and Java curated repositories; JavaScript is in the Premium tier (which comes with Security Command Center Premium or Enterprise).
- Artifact Registry remote repositories can cache upstream packages so builds do not fetch from public indexes directly (see `artifact-registry-repositories`).

## Gotchas
- Policies evaluate by image **digest**; a moving tag that points to an unsigned digest is a failure at deploy time, not at tag push.
- Provenance is generated by Cloud Build; images built elsewhere need their own provenance mechanism.

## Verify
- [ ] A pushed image with a known critical vulnerability shows it in `list-vulnerabilities`, and the CI gate fails.
- [ ] `describe --show-provenance` on a Cloud Build image shows the source and builder details.
- [ ] Deploying an unsigned image to the enforced environment is rejected; the same image with an attestation deploys.

## Checked
2026-10-31. Confirmed against the software supply chain security overview, Binary Authorization overview and attestor CLI page, Cloud Build provenance page and Assured OSS overview: Cloud Build SLSA level 3 provenance and `requestedVerifyOption: VERIFIED` and `--show-provenance`, supported Binary Authorization platforms, Kritis/Grafeas basis, attestation model, continuous validation via check-based platform policies (Preview), Assured OSS languages, tiers and SBOM/VEX formats. The gcloud commands passed the command checker.
Removed as unconfirmed (the scan-containers page cited earlier returns 404): the 30-day rescan claim, Pub/Sub topic name, occurrence kinds list, policy YAML and evaluation-mode names, platform policy check names, break-glass annotation, cosign/Sigstore details, role names, scanner OS coverage list, kube-system gotcha, the `cloud-aoss` registry hostname.
Method: documentation only; no commands were run.
