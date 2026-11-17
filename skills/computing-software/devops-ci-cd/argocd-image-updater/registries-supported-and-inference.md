---
id: computing-software.devops-ci-cd.argocd-image-updater.registries-supported-and-inference
name: registries-supported-and-inference
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, registries, supported-registries, registry-inference, docker-hub, custom-registry, test-command]
level: intro
status: docs-checked
description: "Which registries work out of the box, how the registry is inferred from the image prefix, when a custom entry is needed, and how to test access."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/configuration/registries.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/install/testing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Supported registries and inference

Most registries that implement the Docker registry v2 API work out of the box. Documented as tested: Docker Hub (`docker.io`), the Docker v2 reference registry, Red Hat Quay (`quay.io`), JFrog Artifactory, GitHub Container Registry (`ghcr.io`), GitHub Packages (`docker.pkg.github.com`), GitLab (`registry.gitlab.com`), Google (`gcr.io`) and Azure (`azurecr.io`).

Inference: for `ghcr.io/somerepo/someimage` the updater derives the registry from the `ghcr.io` prefix and uses `https://ghcr.io/v2`. Docker Hub's quirk (prefix `docker.io`, API at `registry-1.docker.io`) is built in.

Configure a custom registry only if:

- it has a self-signed or private TLS certificate (disable verification or add a CA)
- its API endpoint differs from the prefix
- you need a custom rate limit or global credentials
- your cluster's container engine defaults to a registry other than `docker.io`

Find out whether your registry works with no config:

```
argocd-image-updater test myregistry.com/somerepo/someimage
```

Run it from a workstation that can reach the registry or from the controller pod. It makes no changes to your cluster or workloads. Add `--update-strategy` or `--credentials` as needed.

## Checked

2026-11-08. Read in full: docs/configuration/registries.md and docs/install/testing.md. Confirmed the tested registry list, the ghcr.io inference example, the Docker Hub quirk, the four reasons for a custom registry and the test command behaviour. Softened the blanket v2 claim to the docs wording (most registries).

Method: documentation only; no commands were run.
