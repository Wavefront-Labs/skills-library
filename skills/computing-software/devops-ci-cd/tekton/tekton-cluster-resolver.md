---
id: computing-software.devops-ci-cd.tekton.tekton-cluster-resolver
name: tekton-cluster-resolver
category: computing-software
field: devops-ci-cd
product: tekton
tags: [resolvers, cluster-resolver, remote-resolution, namespaces]
level: intro
status: docs-checked
description: "Reference Tekton Tasks, Pipelines and StepActions stored in another namespace with the cluster resolver and understand its caching default."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/cluster-resolver.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resolver type `cluster`. Params: `kind` (`task`, `pipeline`, `stepaction`), `name`, `namespace` (where the resource lives) and optional `cache`.

Caching: the cluster resolver only caches when `cache: always` is given explicitly. `auto`, or leaving it unset, means never cache, because cluster resources have no immutable reference like a git commit or bundle digest. The `cache` param belongs under `pipelineRef.params` or `taskRef.params`.

Global cache size and TTL are set in the `resolver-cache-config` ConfigMap (`max-size` default 1000, `ttl` default 5m); its name can be changed with the `RESOLVER_CACHE_CONFIG_MAP_NAME` environment variable. To change this resolver's default, set `default-cache-mode` (`always`, `never`, `auto`) in `cluster-resolver-config`.

Use the cluster resolver to share common Tasks from a central namespace without copying them into each team namespace.

## Checked

Checked 2026-11-08 against docs/cluster-resolver.md in tektoncd/pipeline (main), read in full. Confirmed resolver type, parameters, cache modes and the explicit-always rule, the cache param placement, resolver-cache-config defaults, RESOLVER_CACHE_CONFIG_MAP_NAME and default-cache-mode. No changes needed to claims.

Method: documentation only; no commands were run.
