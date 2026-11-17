---
id: computing-software.cybersecurity-defensive.cosign.docker-media-types-legacy
name: docker-media-types-legacy
category: computing-software
field: cybersecurity-defensive
product: cosign
tags: [cosign, docker-media-types, registry-support, legacy-registry, oci-media-types]
level: practitioner
status: docs-checked
description: "Sign or attest in registries lacking OCI media types using COSIGN_DOCKER_MEDIA_TYPES=1, plus the README's tested-registry list and reporting."
sources:
  - https://raw.githubusercontent.com/sigstore/cosign/main/README.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_sign.md
  - https://raw.githubusercontent.com/sigstore/cosign/main/doc/cosign_attest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Registries without OCI media types

To sign images in registries which do not yet fully support OCI media types, one may need to use `COSIGN_DOCKER_MEDIA_TYPES` to fall back to legacy equivalents (README). Examples from the README, the sign docs and the attest docs:

```
COSIGN_DOCKER_MEDIA_TYPES=1 cosign sign --key cosign.key legacy-registry.example.com/my/image@$DIGEST
COSIGN_DOCKER_MEDIA_TYPES=1 cosign attest --predicate <FILE> --type <TYPE> --key cosign.key legacy-registry.example.com/my/image
```

Registries the README says cosign has been tested against and works with: AWS Elastic Container Registry, GCP Artifact Registry and Container Registry, Docker Hub, Azure Container Registry, JFrog Artifactory Container Registry, CNCF distribution/distribution, GitLab, GitHub Container Registry, CNCF Harbor, Digital Ocean, Sonatype Nexus, Alibaba Cloud, Red Hat Quay 3.6+ / quay.io, IBM Cloud, Cloudsmith, CNCF zot, OVHcloud Managed Private Registry.

Cosign uses go-containerregistry for registry interactions, which has generally excellent compatibility, but some registries may have quirks. The README asks people to help test and file bugs, with instructions in the tracking issue (sigstore/cosign issue 40).

## Checked

2026-11-04. Confirmed against the cosign README and sign docs (and the attest docs for the attest example): env variable, both examples, registry list, go-containerregistry statement, tracking issue. Removed: the claim that signing or attesting fails (the README says one "may need" the variable), the claim about what exactly it does beyond falling back to legacy equivalents, and the referrers API tag-fallback sentence with its cross-reference to a skill not checked here.
Method: documentation only; no commands were run.
