---
id: computing-software.devops-ci-cd.dagger.container-type-and-caching
name: container-type-and-caching
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, container, cache-volume, dockerfile, oci-labels, terminal, default-address, git-repository]
level: practitioner
status: docs-checked
description: "Use Dagger's Container, CacheVolume and GitRepository types: default image addresses, Dockerfile builds, OCI labels, dependency caches and terminal debugging."
sources: [https://docs.dagger.io/0.21/getting-started/types/container, https://docs.dagger.io/0.21/getting-started/types/cache-volume, https://docs.dagger.io/0.21/getting-started/types/git-repository]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container, CacheVolume and GitRepository types (Dagger 0.21 docs)

Goal: pick the right Container operation, cache dependencies, and debug builds.

A `Container` is the live state of an OCI container managed by the engine, not an image string. Common functions: `from`, `withExec`, `withDirectory`/`withMountedDirectory`, `withFile`/`withMountedFile`, `withMountedCache`, `withEntrypoint`, `withWorkdir`, `withServiceBinding`, `withRegistryAuth`, `withVolatileVariable` (non-secret env that does not invalidate exec cache when only the value changes), `stdout`/`stderr`, `publish`, `export`/`import`, `asTarball`, `asService`, `terminal`.

## Default image address (Go)

A `Container` argument can default to an image; an explicit value overrides it.

```go
func (m *MyModule) Version(
	ctx context.Context,
	// +defaultAddress="alpine:latest"
	ctr *dagger.Container,
) (string, error) {
	return ctr.WithExec([]string{"cat", "/etc/alpine-release"}).Stdout(ctx)
}
```

Python uses a `DefaultAddress` annotation, TypeScript `@argument({ defaultAddress: ... })`, PHP `#[DefaultAddress]`.

## Build from a Dockerfile

`src.DockerBuild().Publish(ctx, "ttl.sh/hello-dagger")`; run with `dagger call build --src="https://github.com/dockersamples/python-flask-redis"`. For a Dockerfile outside the context, copy it in with `WithFile("/src/custom.Dockerfile", dockerfile)` and call `DockerBuild(dagger.DirectoryDockerBuildOpts{Dockerfile: "custom.Dockerfile"})`.

## OCI metadata

`WithAnnotation("org.opencontainers.image.authors", "John Doe")` and `WithLabel("org.opencontainers.image.title", "my-alpine")` before `Publish`.

## Cache dependencies

```go
dag.Container().
	From("golang:1.21").
	WithDirectory("/src", source).
	WithWorkdir("/src").
	WithMountedCache("/go/pkg/mod", dag.CacheVolume("go-mod-121")).
	WithEnvVariable("GOMODCACHE", "/go/pkg/mod").
	WithMountedCache("/go/build-cache", dag.CacheVolume("go-build-121")).
	WithEnvVariable("GOCACHE", "/go/build-cache").
	WithExec([]string{"go", "build"})
```

Cache volumes persist across Dagger sessions. Default cache locations depend on the package manager (`~/.cache/pip`, `~/.cache/pypoetry`).

## Debug with a terminal

Insert `.Terminal()` between steps, for example `From("alpine:latest").Terminal().WithExec(...).Terminal()`; run `dagger call container` and each terminal opens in sequence with full context, also at the failure point. `Directory.Terminal()` defaults to an alpine container; customise with `dagger.DirectoryTerminalOpts{Container: dag.Container().From("ubuntu"), Cmd: []string{"/bin/bash"}}`.

## GitRepository

Functions: `branch`, `commit`, `head`, `ref`, `tag`, `tags`, `branches`. Clone to a container: `dag.Git(repository).Ref(ref).Tree()` then `WithDirectory("/src", d)`. Over SSH pass a `*dagger.Socket`: `dag.Git(repository, dagger.GitOpts{SSHAuthSocket: sock})`, called with `--sock=$SSH_AUTH_SOCK`.

Related: computing-software.devops-ci-cd.dagger.directory-paths-and-filters.

## Checked

2026-11-07

Read in full from the docs source: getting-started/types/container.mdx, cache-volume.mdx and their partials and snippets. Every claim and snippet matched. No corrections needed.

Method: documentation only; no commands were run.
