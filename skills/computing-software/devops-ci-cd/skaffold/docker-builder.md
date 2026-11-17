---
id: computing-software.devops-ci-cd.skaffold.docker-builder
name: docker-builder
category: computing-software
field: devops-ci-cd
product: skaffold
tags: [docker, dockerfile, buildargs, cachefrom, buildkit]
level: intro
status: docs-checked
description: "Build images from a Dockerfile with the docker builder and its common options, including build args and cache sources."
sources:
  - "https://skaffold.dev/docs/builders/builder-types/docker/"
  - "https://skaffold.dev/docs/environment/templating/"
  - "https://skaffold.dev/docs/references/yaml/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `docker` builder builds an image from a Dockerfile locally, in a cluster with Kaniko, or remotely on Google Cloud Build. After a local build, images are pushed to the remote registry unless you skip that.

```yaml
build:
  artifacts:
  - image: my-registry/app
    docker:
      dockerfile: Dockerfile
      buildArgs:
        GO_VERSION: "1.21"
      cacheFrom:
      - my-registry/app:latest
```

Notes from the docs and schema:

- `dockerfile` (default `Dockerfile`) is located relative to the artifact `context`.
- `buildArgs` supports Go templating, so environment variables can be injected, for example `"{{.MY_VERSION}}"`.
- `cacheFrom` lists images used as cache sources; the builder replaces cache references to the artifact image with the tagged image so caching works from the previously built image.
- Other `docker` options include `target`, `noCache`, `pullParent`, `squash`, `network`, `ssh`, `secrets` (needs `useBuildKit: true`), `addHost` and `cliFlags`.
- By default Skaffold talks to the local daemon through the Docker Engine API. `build.local.useDockerCLI: true` uses the `docker` command line instead, which enables BuildKit builds; `build.local.useBuildkit` toggles BuildKit.

Artifact dependencies let one image build on another using `requires`:

```yaml
- image: app
  requires:
  - image: base
    alias: BASE
```

The alias becomes a build arg in the Dockerfile, set to the image built from `base`, so write `ARG BASE` and `FROM $BASE`.

## Checked

2026-11-04. Read the Skaffold Docker Build page, the Templated Fields page and the `DockerArtifact` and `LocalBuild` definitions in the v4beta14 schema. Confirmed the dockerfile default and relative location, templated `buildArgs`, `cacheFrom` rewriting, `requires` alias as a build arg, and the Docker API versus CLI behaviour. Removed: the claim that artifact dependencies are derived from the Dockerfile and `.dockerignore` (not on these pages). The `build.local` field is spelled `useBuildkit` in the schema, while the `secrets` description writes `useBuildKit`.
Method: documentation only; no commands were run.
