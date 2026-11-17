---
id: computing-software.collaboration-platform-administration.vikunja.subdirectory-deployment
name: subdirectory-deployment
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, subpath-hosting, frontend-base, pnpm-build, api-v1-info]
level: advanced
status: docs-checked
description: "Host Vikunja under a URL subpath: rebuild the frontend with VIKUNJA_FRONTEND_BASE, rebuild the binary and route the API through the proxy to the subpath."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/subdirectory.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A subdirectory is not supported out of the box; you must build the frontend yourself (see the build-from-source skill).

Set the base path either way, with `SUBPATH` your directory:

```
VIKUNJA_FRONTEND_BASE=/SUBPATH/ pnpm run build
```

or copy `.env.local.example` to `.env.local`, uncomment `VIKUNJA_FRONTEND_BASE`, set `/subpath/`, and run `pnpm run build`.

Then build the binary as described in building from source.

API: without a reverse proxy, configure the API URL in the frontend as usual. With a proxy, adjust paths so the API is available at `/SUBPATH/api/v1`. Verify by opening `/SUBPATH/api/v1/info` in a browser.

## Checked

2026-11-04. Confirmed against the Vikunja subdirectory page (setup/subdirectory): not supported out of the box, the VIKUNJA_FRONTEND_BASE build command, the .env.local route, building the binary, API URL and proxy path requirement, and the info check. Removed: the claim that the binary build embeds the frontend, which that page does not state.

Method: documentation only; no commands were run.
