---
id: computing-software.devops-ci-cd.turborepo.turbo-json-remote-cache-options-reference
name: turbo-json-remote-cache-options-reference
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, remotecache-config, remote-cache-enabled, signature, preflight, timeout, uploadtimeout, apiurl, loginurl, teamid, teamslug]
level: advanced
status: docs-checked
description: "The remoteCache block: enabled, signature, preflight, timeout, uploadTimeout, apiUrl, loginUrl, teamId and teamSlug, with defaults and rules."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The global `remoteCache` option configures remote cache use:

- **`enabled`** (default `true`): when `false`, all remote cache operations are disabled even with a valid token. When `true` the user must still log in and link the repo.
- **`signature`** (default `false`): sign every uploaded artifact with `TURBO_REMOTE_CACHE_SIGNATURE_KEY`; reject downloaded artifacts with an invalid or missing signature. The docs state this is **not a security feature** but an integrity check, defence in depth against partial uploads or downloads and server issues. Enable `futureFlags.longerSignatureKey` to enforce at least 32 bytes; short keys will be rejected in a future major version.
- **`preflight`** (default `false`): precede any HTTP request with an OPTIONS request to see whether the endpoint supports it.
- **`timeout`** (default `30`): seconds for cache operations, whole values only; `0` means no timeout.
- **`uploadTimeout`** (default `60`): seconds for uploads, whole values only; `0` means no timeout.
- **`apiUrl`** (default `https://vercel.com`): endpoint for API calls.
- **`loginUrl`** (default `https://vercel.com`): endpoint for requesting tokens during `turbo login`.
- **`teamId`**: passed as `teamId` in the query string of all Remote Cache HTTP calls; it must start with `team_` or it is not used.
- **`teamSlug`**: passed as `slug` in the query string.

## Checked

2026-11-04. Read the "Remote caching" section of the configuration reference in full; all nine options, defaults and rules match. Removed the unsupported self-hosting remark and the invented Verify step.

Method: documentation only; no commands were run.
