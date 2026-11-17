---
id: computing-software.cloud-infrastructure-engineering.docker.labels-and-annotations-from-metadata-action
name: labels-and-annotations-from-metadata-action
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, labels, metadata-action-labels, oci-labels, annotations, github-actions, build-push-action]
level: practitioner
status: docs-checked
description: "Generate OCI labels and index annotations with docker/metadata-action: its defaults, customising them, wiring them into build-push-action and checking the result."
sources: ["https://github.com/docker/metadata-action#outputs", "https://github.com/docker/metadata-action#overwrite-labels-and-annotations", "https://docs.docker.com/build/ci/github-actions/annotations/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Labels and annotations from docker/metadata-action

`metadata-action` computes tags **and** a standard set of `org.opencontainers.image.*`
labels from the Git context, so Dockerfiles do not need `ARG`-driven `LABEL` lines.

## Defaults it emits
The README's example output lists `title`, `description`, `url`, `source`, `version`, `created`,
`revision` and `licenses` under `org.opencontainers.image.*`, taken from the repository and
the Git ref (for example `description` from the repository description).

## Workflow
```yaml
- id: meta
  uses: docker/metadata-action@v6
  with:
    images: ghcr.io/${{ github.repository }}
    tags: |
      type=semver,pattern={{version}}
      type=sha
    labels: |
      org.opencontainers.image.vendor=Example Ltd
      org.opencontainers.image.documentation=https://docs.example.com/app
      maintainer=platform-team@example.com
  env:
    DOCKER_METADATA_ANNOTATIONS_LEVELS: manifest,index
- uses: docker/build-push-action@v7
  with:
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
    annotations: ${{ steps.meta.outputs.annotations }}
```
Check the latest major versions of the actions before copying; these were current at the check date.

## Labels vs annotations
- **Labels** are part of the image config (`docker inspect` shows them).
- **Annotations** can be attached to manifests, indexes and descriptors (buildx 0.12 or later).
  By default metadata-action's annotations go on the image manifests
  (`DOCKER_METADATA_ANNOTATIONS_LEVELS` defaults to `manifest`); the README notes that registries
  may expect them elsewhere and that reading annotations at the **index** is common for
  multi-arch images, so set `manifest,index` when you want both.

## Overriding defaults
Keys you set in `labels:` (or `annotations:`) overwrite the generated ones, for example
`org.opencontainers.image.title=MyCustomTitle`.

## Verify
```bash
docker buildx imagetools inspect ghcr.io/org/app:1.2.0 --raw
docker pull ghcr.io/org/app:1.2.0 && docker image inspect -f '{{json .Config.Labels}}' ghcr.io/org/app:1.2.0
```

## Gotchas
- `created` changes every build; the README shows setting it from the commit date
  (`{{commit_date ...}}`) when you need stable values.
- The build must produce the components you annotate: asking for `index` annotations when the
  build produces only a manifest makes the build fail (Docker's annotations guide).

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), Compose file reference, tini, Trivy and metadata-action documentation. Confirmed against the metadata-action README (v6.2.0 current) and Docker's annotations guide: current majors (metadata-action v6, build-push-action v7), default label keys from the example output, annotations output and DOCKER_METADATA_ANNOTATIONS_LEVELS (default manifest), overwrite behaviour, commit_date example for created, and the failure when index annotations are requested for a manifest-only build. Removed unconfirmed claims about which registries read index annotations, dropping a default with an empty value, the classic-driver limitation and the jq pipelines.

Method: documentation only; no commands were run.
