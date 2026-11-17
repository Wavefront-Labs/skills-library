---
id: computing-software.devops-ci-cd.dagger.cookbook-build-and-publish-images
name: cookbook-build-and-publish-images
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, cookbook, builds, multi-stage, multi-arch, dockerfile, publish, registry, oci-labels, env-vars]
level: practitioner
status: docs-checked
description: "Dagger cookbook recipes for multi-stage, matrix, multi-arch and Dockerfile builds, OCI annotations and labels, registry publishing with tags, and image export."
sources: [https://docs.dagger.io/0.21/cookbook/builds, https://docs.dagger.io/0.21/cookbook/containers]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger cookbook: build and publish images

Goal: pick the right recipe for building artifacts and publishing images. Go code below is from the Dagger 0.21 cookbook snippets; Python and TypeScript variants exist.

## Multi-stage build
Build in a `golang:latest` builder (`CGO_ENABLED=0`, `go build -o myapp`), copy the binary into `alpine` with `WithFile("/bin/myapp", builder.File("/src/myapp"))`, set `WithEntrypoint`, then `Publish(ctx, "ttl.sh/myapp:latest")`. Run: `dagger call build --src="https://github.com/golang/example#master:hello"`.

## Matrix build
Loop over OS and architecture, set `GOOS`/`GOARCH` env vars per `WithExec`, collect each result into one directory with `outputs.WithDirectory(path, build.Directory(path))` (paths like `build/linux/amd64/`). Export with `dagger call build --src=... export --path=/tmp/matrix-builds`; expect darwin and linux, each with amd64 and arm64 (4 files).

## Multi-arch image
Two approaches, both publish with `Publish(ctx, "ttl.sh/myapp:latest", dagger.ContainerPublishOpts{PlatformVariants: variants})`:
- Emulation: `dag.Container(dagger.ContainerOpts{Platform: platform})` for each of `linux/amd64`, `linux/arm64`, `linux/s390x`; build with `CGO_ENABLED=0` in `golang:1.20-alpine`, then wrap `/output` via `WithRootfs`.
- Cross-compilation: build on the host platform (omit platform), set `GOOS=linux` and `GOARCH` from `dag.Containerd().ArchitectureOf(ctx, platform)`, then wrap the output in a container for the target platform with `WithEntrypoint("/hello")`. Needs `dagger install github.com/levlaz/daggerverse/containerd@v0.1.2`.

## Dockerfile builds
`src.DockerBuild().Publish(ctx, "ttl.sh/hello-dagger")`. For a Dockerfile outside the build context, copy it in and name it: `DockerBuild(dagger.DirectoryDockerBuildOpts{Dockerfile: "custom.Dockerfile"})`. Dockerfile as a remote ref: `--dockerfile=https://github.com/vimagick/dockerfiles#master:registry-cli/Dockerfile`.

## OCI metadata
- Annotations: `WithAnnotation("org.opencontainers.image.authors", "John Doe")`, `WithAnnotation("org.opencontainers.image.title", ...)`.
- Labels: `WithLabel("org.opencontainers.image.title", "my-alpine")`, `.version`, `.created`, `.source`, `.licenses`.

## Environment variables
`WithEnvVariable("ENV_VAR", "VALUE")` for one; for many, a helper of type `dagger.WithContainerFunc` looping `WithEnvVariable` applied via `.With(EnvVariables([...]))`. Use `withSecretVariable` for sensitive values and `withVolatileVariable` (expert only) for exec-time metadata that must not decide cache reuse; volatile variables are visible only to later `withExec`, are not in the image config and not returned by `envVariable(s)`.

## Publish to a private registry
Take `registry`, `username` and `password *dagger.Secret`; call `WithRegistryAuth(registry, username, password)` then `Publish(ctx, fmt.Sprintf("%s/%s/my-nginx", registry, username))`. Run `dagger call publish --registry=docker.io --username=user --password=env://PASSWORD` (also `ghcr.io` with a personal access token). For several tags loop over `["latest","1.0-alpine","1.0","1.0.0"]` publishing `.../my-nginx:<tag>`.

## Export an image
`dagger call base export-image --name myimage` loads it into Docker; `dagger call base export --path=/path/to/mycontainer.tgz` writes an OCI tarball.

Related: cache-volumes-dependencies, secrets-handling-and-caching, error-handling-and-debugging (concurrent steps).

## Checked

2026-11-07

Read in full from the docs source: cookbook/builds.mdx and cookbook/containers.mdx with partials and snippets. Every claim and snippet matched. No corrections needed.

Method: documentation only; no commands were run.
