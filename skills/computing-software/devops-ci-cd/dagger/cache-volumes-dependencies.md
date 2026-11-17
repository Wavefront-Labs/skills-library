---
id: computing-software.devops-ci-cd.dagger.cache-volumes-dependencies
name: cache-volumes-dependencies
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, cache-volumes, dependencies, npm, go-modules, pip, build-speed, cache-invalidation]
level: practitioner
status: docs-checked
description: "Mount Dagger cache volumes for npm, Go and pip dependencies, and invalidate layer cache with a cache-buster variable when needed."
sources: [https://docs.dagger.io/0.21/extending/cache-volumes, https://docs.dagger.io/0.21/cookbook/builds]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cache volumes for package managers

Goal: reuse downloaded dependencies across Dagger Function runs. Dagger 0.21 docs.

## npm (Go module code)
```go
func (m *MyModule) Build(source *dagger.Directory) *dagger.Container {
	return dag.Container().
		From("node:21").
		WithDirectory("/src", source).
		WithWorkdir("/src").
		WithMountedCache("/root/.npm", dag.CacheVolume("node-21")).
		WithExec([]string{"npm", "install"})
}
```
The first run is slow; later runs reuse the volume if nothing else changed. Shell form: `container | from node:21 | with-directory /src https://github.com/dagger/hello-dagger | with-workdir /src | with-mounted-cache /root/.npm node-21 | with-exec npm install`.

## Go
Mount two volumes and point Go at them:
```go
WithMountedCache("/go/pkg/mod", dag.CacheVolume("go-mod-121")).
WithEnvVariable("GOMODCACHE", "/go/pkg/mod").
WithMountedCache("/go/build-cache", dag.CacheVolume("go-build-121")).
WithEnvVariable("GOCACHE", "/go/build-cache").
WithExec([]string{"go", "build"})
```

## Python
The default cache directory depends on the package manager: `~/.cache/pip` for pip, `~/.cache/pypoetry` for poetry. The cookbook mounts `/root/.cache/pip` (volume `pip_cache`) and `/root/.cache/pypoetry` (volume `poetry_cache`), then runs `poetry install --no-root --no-interaction` followed by `poetry install --no-interaction --only-root`.

Run with `dagger call build --source=.`.

## Scope
Cache volumes are scoped to the module that defines them. To share one across modules, pass a reference through constructor or function arguments.

## Forcing a rerun (layer cache)
Inject a volatile value at the exact step that must rerun:
```go
WithEnvVariable("CACHEBUSTER", time.Now().String()).
WithExec([]string{"date"})
```
Remove the variable and the first run's output is returned every time. The cookbook calls this a temporary workaround until official invalidation exists, and notes that changes to mounted cache volumes or secrets do not invalidate the layer cache.

Related: function-caching-policies; services-bind-expose-lifecycle (persisting Redis state via a volume).

## Checked

2026-11-07

Read in full from the docs source: extending/modules/cache-volumes.mdx and cookbook/builds.mdx with its embedded partials (_cache-dependencies.mdx, _invalidate-cache.mdx) and their Go and Python snippet files. Confirmed the npm, Go (GOMODCACHE, GOCACHE) and pip/poetry mounts and volume names, the poetry install commands, module scoping of cache volumes, the CACHEBUSTER example and both cookbook notes. No corrections needed.

Method: documentation only; no commands were run.
