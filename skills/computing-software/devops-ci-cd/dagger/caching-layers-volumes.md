---
id: computing-software.devops-ci-cd.dagger.caching-layers-volumes
name: caching-layers-volumes
category: computing-software
field: devops-ci-cd
product: dagger
tags: [dagger, caching, cache-volume, layers, performance, npm, apt]
level: practitioner
status: docs-checked
description: "Speed up Dagger workflows with layer caching and cache volumes for package manager caches such as npm and apt, using CacheVolume and WithMountedCache."
sources: [https://docs.dagger.io/0.21/introduction/features/caching, https://docs.dagger.io/0.21/getting-started/quickstarts/basics, https://docs.dagger.io/0.21/getting-started/quickstarts/ci/, https://docs.dagger.io/0.21/introduction/features/observability]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dagger caching: layers and cache volumes

Goal: make repeat runs fast by using Dagger's caches deliberately (Dagger 0.21 docs).

## What is cached

1. Layers: build instructions and results of some API calls (those modifying files and directories). Before running a function Dagger checks whether the needed layers exist and reuses them if inputs are unchanged.
2. Volumes: contents of a Dagger filesystem volume, persisted across Engine sessions.
3. Function calls: return values of module functions may skip execution when a cached result exists (details are in the Extending Dagger function-caching page, not covered here).

## When to use a cache volume

Package managers (`npm`, `maven`, `pip` and similar) keep their own cache directory. Persist that directory in a cache volume so dependencies are not re-downloaded each session.

## Pattern (Go)

```go
func (m *Basics) Env(ctx context.Context) *dagger.Container {
	aptCache := dag.CacheVolume("apt-cache")
	return dag.Container().
		From("debian:latest").
		WithMountedCache("/var/cache/apt/archives", aptCache).
		WithExec([]string{"apt-get", "update"}).
		WithExec([]string{"apt-get", "install", "--yes", "maven", "mariadb-server"})
}
```
The CI quickstart does the same for npm: `dag.CacheVolume("node")` mounted at `/root/.npm` before `npm install`. Python: `dag.cache_volume(...)` and `.with_mounted_cache(path, vol)`; TypeScript: `dag.cacheVolume(...)` and `.withMountedCache(path, vol)`.

Calling the function repeatedly shows the second and later runs drastically faster than the first. Cached steps appear as cached in the terminal UI and Dagger Cloud traces.

Related: `computing-software.devops-ci-cd.dagger.ci-workflow-quickstart`, `computing-software.devops-ci-cd.dagger.debug-observability`.

## Checked

2026-11-07

Read in full from the docs source: introduction/features/caching.mdx, getting-started/quickstarts/basics/index.mdx (Speed things up section, apt example) and the CI quickstart snippets (node cache at /root/.npm). The terminal UI statement is supported by introduction/features/observability.mdx (cached and pending states), so that page was added to sources. Dagger Cloud showing whether operations were cached is stated in the quickstart pages.

Method: documentation only; no commands were run.
