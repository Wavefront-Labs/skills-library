---
id: computing-software.devops-ci-cd.tekton.tekton-http-resolver
name: tekton-http-resolver
category: computing-software
field: devops-ci-cd
product: tekton
tags: [resolvers, http-resolver, digest, remote-resolution]
level: practitioner
status: docs-checked
description: "Fetch a Tekton resource over HTTP or HTTPS with the http resolver, using basic auth credentials and digest verification."
sources:
  - https://github.com/tektoncd/pipeline/blob/main/docs/http-resolver.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resolver type `http`. Params: `url` (HTTP or HTTPS only), `http-username` with `http-password-secret` (and optional `http-password-secret-key`) for authenticated fetches, and `digest` to verify content integrity in the form `<algorithm>:<hash>` with `sha256` or `sha512`.

Compute a digest locally:

```bash
curl -sL https://raw.githubusercontent.com/owner/private-repo/main/task/task.yaml | sha256sum
curl -sL https://raw.githubusercontent.com/owner/private-repo/main/task/task.yaml | sha512sum
```

Requirements: v0.41.0 or later, resolvers installed, `enable-http-resolver: "true"` in `resolvers-feature-flags` (namespace `tekton-pipelines-resolvers`), beta features on. Config: `fetch-timeout` (a global 1 minute maximum applies to all resolution requests).

## Checked

2026-11-03. Prose, field names, defaults, flags and limits confirmed against the Tekton Pipelines docs page(s): http-resolver.md. Removed: the closing digest tip.

Method: documentation only; no commands were run.
