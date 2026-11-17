---
id: computing-software.devops-ci-cd.gitlab-runner.runner-feature-flags
name: runner-feature-flags
category: computing-software
field: devops-ci-cd
product: gitlab-runner
tags: [feature-flags, ff, environment-variable, deprecation]
level: practitioner
status: docs-checked
description: "How runner feature flags are enabled and which defaults matter."
sources: ["https://docs.gitlab.com/runner/configuration/feature-flags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Feature flags

Feature flags toggle behaviour changes. Enable or disable them with environment variables set to `"true"` or `1` to activate. Set them in the job `variables:`, the runner `environment` setting, or the runner process environment.

Examples:
- `FF_USE_ADAPTIVE_REQUEST_CONCURRENCY`: default `true`; `request_concurrency` becomes the maximum and the number of concurrent requests adjusts to the job-request success rate.
- `FF_USE_FASTZIP`: default `true`; deprecated, with the flag and the legacy zip implementation removed in 19.9.
- `FF_HASH_CACHE_KEYS`: default `false`; hashes (SHA256) cache keys before use.
- `FF_USE_PARALLEL_CACHE_TRANSFER`: default `false`; parallel object storage transfers for cache uploads and downloads.
- `FF_NETWORK_PER_BUILD`: default `false`; creates a Docker network per build with the docker executor.

Check the feature flags table for deprecations and removal versions.

## Checked

2026-11-03. Confirmed against flag defaults and descriptions in the Feature flags table. Removed: the false/0 value claim (page states only how to activate) and the generic regression tip.

Method: documentation only; no commands were run.
