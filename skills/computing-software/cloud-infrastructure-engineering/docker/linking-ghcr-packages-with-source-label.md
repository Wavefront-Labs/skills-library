---
id: computing-software.cloud-infrastructure-engineering.docker.linking-ghcr-packages-with-source-label
name: linking-ghcr-packages-with-source-label
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, labels, ghcr-source-label, ghcr, github-packages, org-opencontainers-image, oci-labels]
level: practitioner
status: docs-checked
description: "Connect a GHCR container package to its repository via org.opencontainers.image.source so it inherits repo permissions and shows README, description and licence."
sources: ["https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry", "https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking GHCR packages with the source label

A package pushed from the command line to `ghcr.io/<owner>/<name>` is not linked to a repository by
default, even if the name matches the repository. GitHub's guidance: add the
`org.opencontainers.image.source` label to the Dockerfile so the package connects to the repository
and the workflow `GITHUB_TOKEN` gets the right permissions. Publishing from a workflow with
`GITHUB_TOKEN` links the workflow's repository automatically, but that token will not be able to
push if you previously pushed a package to the same namespace without connecting it.

## Labels GHCR reads
| Label | Effect on GHCR |
|---|---|
| `org.opencontainers.image.source=https://github.com/<owner>/<repo>` | Repository associated with the package |
| `org.opencontainers.image.description=...` | Text-only description shown on the package page (limit 512 characters) |
| `org.opencontainers.image.licenses=MIT` | SPDX licence identifier shown in the Details sidebar (limit 256 characters) |

```dockerfile
LABEL org.opencontainers.image.source=https://github.com/example/api
LABEL org.opencontainers.image.description="Example API server"
LABEL org.opencontainers.image.licenses=Apache-2.0
```
Or at build time: `docker build --label "org.opencontainers.image.source=https://github.com/example/api" .`

## Multi-arch images
For a multi-arch image the package-page description comes from the `annotations` field of the
image manifest, not from Docker labels. The GitHub docs set it with build-push-action:
```yaml
outputs: type=image,name=target,annotation-index.org.opencontainers.image.description=My multi-arch image
```

## After linking
- A package linked to a repository inherits that repository's access permissions, and Actions
  workflows in the repository get access to the package, unless the organization has disabled
  automatic inheritance.
- Visibility is separate: the default visibility on first publish is private.
- You can also link in the UI: package page > "Connect repository". To move a package to another
  repository, unlink it (package settings > "Repository source") and link it again.

## Verify
Push a new tag and check the package page shows the repository link, README, description and licence.

## Checked
Checked 2026-10-28 against GitHub Docs "Working with the Container registry" and "Connecting a
repository to a package": the three label keys, the 512 and 256 character limits, the multi-arch
annotation behaviour, default private visibility, permission inheritance, and the connect, unlink
and migrate steps. Removed because the docs do not state them: that only the creator can manage an
unlinked package, a "Manage Actions access" menu path, that `.git` or SSH URLs fail to link, the
sidebar "Packages" placement, the `docker/metadata-action` behaviour and the `imagetools --raw` check.
Method: documentation only; no commands were run.
