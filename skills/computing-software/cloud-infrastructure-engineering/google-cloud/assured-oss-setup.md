---
id: computing-software.cloud-infrastructure-engineering.google-cloud.assured-oss-setup
name: assured-oss-setup
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, software-supply-chain, assured-oss-setup, assured-open-source-software, artifact-registry, remote-repositories]
level: practitioner
status: docs-checked
description: "Consume Google's Assured Open Source Software packages for Java and Python: enable access, authenticate pip and Maven, use virtual repositories, and read the metadata."
sources: ["https://cloud.google.com/assured-open-source-software/docs/overview", "https://cloud.google.com/assured-open-source-software/docs/download-python-packages", "https://cloud.google.com/assured-open-source-software/docs/download-java-packages", "https://cloud.google.com/assured-open-source-software/docs/validate-metadata"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Assured OSS setup

Assured OSS gives Google-built, signed, scanned builds of popular Java and Python packages, with SBOM,
provenance and VEX metadata. There is a Free tier and a Premium tier (Premium comes with Security Command Center Premium or Enterprise).

## 1. Access
For the free tier, submit the customer enablement form to enable access. The free-tier pages authenticate with a service account key (base64-encoded), which needs `roles/iam.serviceAccountKeyAdmin` on the organization to obtain. Follow the current download pages for the exact steps.

## 2. Python
```bash
pip install keyrings.google-artifactregistry-auth
pip install --index-url https://us-python.pkg.dev/cloud-aoss/cloud-aoss-python/simple/ requests==2.32.3
```
The docs also describe setting up virtual repository access; use it so builds prefer Assured builds transparently.

## 3. Java (Maven)
`settings.xml` / `pom.xml`:
```xml
<repository>
  <id>artifact-registry</id>
  <url>artifactregistry://us-maven.pkg.dev/cloud-aoss/cloud-aoss-java</url>
</repository>
```
with the `artifactregistry-maven-wagon` build extension (see the Java download page).

## 4. Metadata
Packages come with signed provenance, an SBOM (SPDX) and VEX information (CycloneDX). Validate metadata as described in the "Validate metadata" docs, and archive the SBOM with your release.

## Gotchas
- Mixing fallback to public indexes defeats the point for critical builds: alert when fallback is used.
- `--require-hashes` is optional, but if used, every package in requirements.txt needs hashes; the Python download page documents where the Assured artifact hashes live.

## Verify
- [ ] `pip download` / `mvn dependency:resolve -X` logs show resolution from the Assured OSS repo; metadata validation passes.

## Checked

2026-10-28. Confirmed against: Assured OSS overview (tiers, SPDX, CycloneDX VEX, signed provenance), free-tier Python page (pip keyring package, us-python index URL, --require-hashes, hash location) and Java page (us-maven URL, maven wagon, enablement form, serviceAccountKeyAdmin).

Removed or rewritten: the roles/artifactregistry.reader grant and repository names, remote-repo-with-fallback advice, SLA wording, the signature/public-key step and the claim that not every version is built; none appeared in the fetched pages.

Method: documentation only; no commands were run.
