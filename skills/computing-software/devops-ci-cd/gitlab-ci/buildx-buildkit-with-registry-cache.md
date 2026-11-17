---
id: computing-software.devops-ci-cd.gitlab-ci.buildx-buildkit-with-registry-cache
name: buildx-buildkit-with-registry-cache
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, buildx-gitlab, buildkit-cache-registry, cache-to-registry]
level: practitioner
status: docs-checked
description: "Build images in GitLab CI with docker buildx (BuildKit) and the registry cache backend: ref, mode min or max, OCI manifest options, and the separate-cache-ref rule."
sources: ["https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/ci/", "https://docs.gitlab.com/ci/docker/using_docker_build/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# buildx / BuildKit with registry cache

## 1. Job shape
```yaml
build:
  image: docker:<version>
  services: [docker:<version>-dind]     # see the GitLab Docker build page for dind variables
  variables:
    CACHE_REF: $CI_REGISTRY_IMAGE/cache:buildx
  before_script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login "$CI_REGISTRY" -u "$CI_REGISTRY_USER" --password-stdin
  script:
    - docker buildx build
        --cache-from "type=registry,ref=$CACHE_REF"
        --cache-to "type=registry,ref=$CACHE_REF,mode=max"
        --tag "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
        --push .
```
A dind job starts with no layer store, so the registry cache is what makes rebuilds fast.
Registry cache works with the default `docker` driver only when the containerd image store is
enabled; otherwise use another driver (for example `docker-container` via
`docker buildx create --use`). See Docker's "Build drivers".

## 2. Registry cache parameters (from the Docker docs)
| name | where | values | default |
|---|---|---|---|
| `ref` | to and from | full cache image name | required |
| `mode` | to | `min`, `max` | `min` |
| `oci-mediatypes` | to | true, false | true |
| `image-manifest` | to | true, false | true |
| `compression` | to | gzip, estargz, zstd | gzip |
| `compression-level` | to | 0..22 | unset |
| `force-compression` | to | true, false | false |
| `ignore-error` | to | boolean | false |

- `max` mode can cache multi-stage builds fully, instead of only the final stage.
- `ref` must differ from the image's push target; use a different tag, image name or
  repository for the cache.
- If the `--cache-from` target does not exist the import step fails but the build continues.
- Registry cache keeps the cache separate from the image, so the final image ships without it,
  and it works with exporters other than the image exporter.

## Verify
- [ ] Second run reuses unchanged steps and the registry shows the cache tag.

## Checked
2026-10-31. Confirmed on the Docker registry cache page (parameters table, defaults,
driver note, separate ref rule, missing-ref behaviour) and the Docker CI page.
Removed as unconfirmed: provenance flag, per-branch cache scheme, multi-platform binfmt and
emulation slowdown figures, `imagetools` merge advice, cache-mount export claim, dind TLS
variable values, specific Docker image versions.
Method: documentation only; no commands were run.
