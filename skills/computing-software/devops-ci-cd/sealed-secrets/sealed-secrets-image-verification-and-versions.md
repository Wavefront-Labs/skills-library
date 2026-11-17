---
id: computing-software.devops-ci-cd.sealed-secrets.sealed-secrets-image-verification-and-versions
name: sealed-secrets-image-verification-and-versions
category: computing-software
field: devops-ci-cd
product: sealed-secrets
tags: [sealed-secrets, cosign, image-signing, supported-versions, kubernetes-compatibility, upgrade, release-notes]
level: practitioner
status: docs-checked
description: "Verify Sealed Secrets controller images with cosign and understand supported versions, Kubernetes compatibility and upgrade guidance."
sources: ["https://github.com/bitnami/sealed-secrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sealed secrets image verification and versions

Image signing. Controller images are signed with cosign and the signatures are stored in GitHub Container Registry. Images up to and including v0.20.2 were signed with Cosign v1; newer images use Cosign v2. Verify with:

```bash
export COSIGN_REPOSITORY=ghcr.io/bitnami/sealed-secrets-controller/signs
cosign verify --key .github/workflows/cosign.pub ghcr.io/bitnami/sealed-secrets-controller:latest
cosign verify --key .github/workflows/cosign.pub docker.io/bitnami/sealed-secrets-controller:latest
```

The public key file comes from the project repository.

Versions and upgrades. Only the latest Sealed Secrets release is supported for production. Read RELEASE-NOTES.md before upgrading the client or controller since breaking changes are recorded there.

Kubernetes compatibility. The controller relies on stable Kubernetes APIs; versions above 1.16 are generally considered compatible, officially supported versions are those currently recommended on the Kubernetes releases page, and versions above 1.24 are verified in CI for every release.

Versioning schemes differ: the controller uses 0.X.Y while the Helm chart uses 1.X.Y-rZ, so a chart revision does not map one-to-one to a controller release.

## Checked
Date: 2026-11-04. Documentation: bitnami-labs/sealed-secrets README (raw markdown, main branch), sections How to verify the images, Upgrade, Supported Versions, Compatibility with Kubernetes versions, Helm Chart.
Confirmed: cosign signing, `COSIGN_REPOSITORY`, verify commands, Cosign v1 up to v0.20.2, latest-only support, Kubernetes 1.16 / 1.24 statements, version schemes.
Removed: nothing.
Method: documentation only; no commands were run.
