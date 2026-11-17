---
id: computing-software.devops-ci-cd.gitlab-ci.rootless-buildah-builds
name: rootless-buildah-builds
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, buildah-rootless, buildah-gitlab, oci-image-build]
level: advanced
status: docs-checked
description: "Build OCI images with buildah in GitLab CI: isolation types, image format, layer caching with --layers/--cache-from/--cache-to, and multi-platform manifests."
sources: ["https://github.com/containers/buildah/blob/main/docs/buildah-build.1.md", "https://docs.gitlab.com/ci/docker/using_docker_build/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Buildah builds in GitLab CI

## 1. Job
```yaml
build-buildah:
  image: <buildah image>              # an image that contains buildah
  variables:
    BUILDAH_ISOLATION: chroot         # or rootless; see section 2
    BUILDAH_FORMAT: oci
  script:
    - echo "$CI_REGISTRY_PASSWORD" | buildah login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - buildah build --layers
        --cache-from "$CI_REGISTRY_IMAGE/cache" --cache-to "$CI_REGISTRY_IMAGE/cache"
        -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" .
    - buildah push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
```
GitLab's Docker build page notes that you can build images without enabling privileged mode
on the runner; check that page for the current options.

## 2. Isolation and format (buildah-build man page)
- `--isolation` (or `BUILDAH_ISOLATION`): `oci` (default), `rootless` (default for unprivileged
  users; private IPC, PID, mount and user namespaces) and `chroot` (an internal wrapper reusing
  the host's cgroup, network, IPC and PID namespaces and creating user namespaces only when ID
  mapping needs them).
- `--format` (or `BUILDAH_FORMAT`): `oci` (default) or `docker`.

## 3. Caching
- `--layers` caches intermediate images (default false). By default only one new layer is added
  on top of the base image.
- `--cache-to` pushes cache content to a remote repository; `--cache-from` reads it. Both are
  ignored unless `--layers` is set. Example from the man page:
  `buildah build -t test --layers --cache-to registry/myrepo/cache --cache-from registry/myrepo/cache .`
- `--save-stages` with `--layers` lets later builds reuse intermediate layers.

## 4. Multi-platform
`--platform` takes a comma-separated list or repeats; with more than one platform use `--manifest`
instead of `--tag`, and it cannot be combined with `--arch`, `--os` or `--variant`. The man page
notes multi-architecture builds need emulation software.
```bash
buildah build --platform linux/amd64,linux/arm64 --manifest "$CI_REGISTRY_IMAGE:$TAG" .
```

## Verify
- [ ] The job builds and pushes on a runner without privileged mode, or you have recorded why not.

## Checked
2026-10-31. Confirmed in the buildah-build man page: isolation types and env var, format and
env var, --layers default, --cache-from and --cache-to behaviour and example, --platform and
--manifest rules, emulation note.
Removed as unconfirmed: pinned image tag, STORAGE_DRIVER vfs/overlay table and speeds, kernel
version requirement, /dev/fuse advice, `manifest push` command, error messages, ephemeral storage advice.
Method: documentation only; no commands were run.
