---
id: computing-software.devops-ci-cd.turborepo.remote-caching-self-hosting-and-api-spec
name: remote-caching-self-hosting-and-api-spec
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, remote-cache-api, self-hosted-cache, turbo-login-manual, openapi, v8-endpoints, community-implementations, vercel-remote-cache-sdk]
level: advanced
status: docs-checked
description: "Self-host a Turborepo Remote Cache, log in with turbo login --manual, follow the OpenAPI v8 spec, and know the listed community servers."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/core-concepts/remote-caching.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/system-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Any HTTP server that meets Turborepo's Remote Caching API specification can act as a Remote Cache.

**Managed:** Vercel provides a managed Remote Cache, zero-configuration, integrated with Vercel deployments through the open-source Vercel Remote Cache SDK.

**Self-hosting:** log in with the `--manual` flag to provide the API URL, team and token:

```bash
turbo login --manual
```

**Spec:** an OpenAPI specification is published as a human-readable viewer and as JSON. At the time of the docs, all versions of `turbo` are compatible with the **`v8` endpoints**.

**Community implementations** listed: `brunojppb/turbo-cache-server`, `ducktors/turborepo-remote-cache`, and `Tapico/tapico-turborepo-remote-cache`.

Related `turbo.json` settings from the configuration reference (`remoteCache` block): `apiUrl` (default `https://vercel.com`) sets the endpoint for API calls, `loginUrl` (default `https://vercel.com`) sets the endpoint for requesting tokens during `turbo login`, `teamId` must start with `team_` or it is not used, and `teamSlug` is passed as `slug` in the query string. `enabled: false` disables all remote cache operations even with a valid token. Timeouts default to 30 seconds for operations and 60 seconds for uploads, whole values only. In CI, supply `TURBO_TOKEN` (the Bearer token) and `TURBO_TEAM` (the account name; with Vercel Remote Cache your team's slug) as environment variables.

## Checked

2026-11-04. Read the Remote Cache API section of the Remote Caching page in full, the `remoteCache` section of the configuration reference, and `TURBO_TOKEN`/`TURBO_TEAM` in the system environment variables reference. All defaults, the `team_` prefix rule, `slug` query string, timeouts, the `v8` note and the three community servers match. Removed the invented Verify step.

Method: documentation only; no commands were run.
