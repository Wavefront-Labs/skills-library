---
id: computing-software.cybersecurity-defensive.trivy.air-gapped-and-restricted-network-trivy
name: air-gapped-and-restricted-network-trivy
category: computing-software
field: cybersecurity-defensive
product: trivy
tags: [air-gap, offline-scan, skip-version-check, disable-telemetry, vex-hub, maven-central, check-trivy-dev]
level: sme
status: docs-checked
description: "List every external resource Trivy contacts and configure it for restricted or fully air-gapped networks."
sources:
  - https://trivy.dev/latest/docs/guide/advanced/air-gap/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Trivy normally needs internet access. The external resources and the features that use them:
- vulnerability database: vulnerability scanning;
- Java vulnerability database: Java scanning;
- checks bundle: misconfiguration scanning;
- VEX Hub: VEX repository support;
- Maven Central and remote repositories: Java vulnerability scanning;
- remote Terraform modules: Terraform misconfiguration scanning.

Databases are OCI images on public registries following the OCI Distribution spec. Known hosts: `mirror.gcr.io` and `googlecode.l.googleusercontent.com` (Google), `ghcr.io` and `pkg-containers.githubusercontent.com` (GitHub). Host copies in your own registry (see the self-hosting skill).

The checks bundle is embedded in the binary at build time, so misconfiguration scanning still works air-gapped with checks from your Trivy release. VEX Hub is fetched over plain HTTPS from GitHub (`api.github.com`, `codeload.github.com`) and can be mirrored.

Maven Central (`https://repo.maven.apache.org/maven2`) cannot be used offline; avoid the attempt with `--offline-scan`.

Update and telemetry traffic goes to `https://check.trivy.dev` and is optional. Disable both, because one flag alone is not enough:
```bash
trivy image --skip-version-check --disable-telemetry <image>
```
Public infrastructure can rate limit you under extreme load.

## Checked

2026-11-03. Read and confirmed against the Connectivity and Network considerations (air-gap) page on trivy.dev: the commands, flags, field names, defaults and behaviours stated above. Removed: nothing.

Method: documentation only; no commands were run.
