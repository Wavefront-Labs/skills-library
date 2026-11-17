---
id: computing-software.systems-network-administration.audiobookshelf.ssrf-filter-and-local-podcasts
name: ssrf-filter-and-local-podcasts
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [ssrf, podcasts, environment-variables, disable-ssrf-request-filter, whitelist]
level: practitioner
status: docs-checked
description: "Add a podcast hosted on a local IP by disabling or whitelisting the SSRF request filter in Audiobookshelf."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/podcast-library/1.podcast-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default Audiobookshelf refuses to add a podcast that is hosted on a local IP address. This is a mitigation for server-side request forgery (SSRF). If you self-host the podcast on the same network, the add fails until you relax the filter.

Options from the environment page:

- `DISABLE_SSRF_REQUEST_FILTER=1` (default `'0'`) turns the filter off. The docs' own note for self-hosting a podcast from the same server:

```bash
-e DISABLE_SSRF_REQUEST_FILTER=1
```

- `SSRF_REQUEST_FILTER_WHITELIST` takes a comma-separated list of domains to exclude from the filter, a narrower choice than disabling it entirely.
- `EXP_PROXY_SUPPORT` also disables the filter as a side effect.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Environment Configuration page (Security note, Security table) and the podcast library structure page (Adding a podcast).

Method: documentation only; no commands were run.
