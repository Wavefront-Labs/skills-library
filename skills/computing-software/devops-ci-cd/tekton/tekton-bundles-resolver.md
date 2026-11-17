---
id: computing-software.devops-ci-cd.tekton.tekton-bundles-resolver
name: tekton-bundles-resolver
category: computing-software
field: devops-ci-cd
product: tekton
tags: [resolvers, bundles-resolver, oci, remote-resolution]
level: practitioner
status: docs-checked
description: "Pull Tekton Tasks and Pipelines from OCI bundle images with the bundles resolver, including params, service account defaults, caching and cache sizing."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/bundle-resolver.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resolver type `bundles`. Params: `bundle` (image URL, for example `gcr.io/tekton-releases/catalog/upstream/golang-build:0.1`), `name` (resource in the bundle), `kind` (for example `task`), `secret` (registry credentials secret) and `cache`.

Requirements: v0.41.0 or later, resolvers installed, `enable-bundles-resolver: "true"` in `resolvers-feature-flags` in `tekton-pipelines-resolvers`, beta features on.

Config options: `default-service-account` (default `default`), `default-kind` (`task`), and the same backoff settings as the other resolvers (`backoff-duration` 2s, `backoff-factor` 2.0, `backoff-jitter` 0.1, `backoff-steps` 2, `backoff-cap` 10s).

Caching: `auto` (default) caches only bundles pulled by digest, because tags are mutable; `always` and `never` override that. The `cache` param goes under `taskRef.params` or `pipelineRef.params`. Cache size and lifetime are global in the `resolver-cache-config` ConfigMap: `max-size` (default 1000 entries) and `ttl` (default 5m).

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): bundle-resolver.md. Removed: the closing digest-pinning tip.

Method: documentation only; no commands were run.
