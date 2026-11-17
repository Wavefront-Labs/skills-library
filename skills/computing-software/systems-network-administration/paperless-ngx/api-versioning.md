---
id: computing-software.systems-network-administration.paperless-ngx.api-versioning
name: api-versioning
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, api-version, accept-header, x-api-version, deprecation, client-compatibility]
level: practitioner
status: docs-checked
description: "Pin the Paperless-ngx API version with the Accept header and check server compatibility from the response headers."
sources:
  - "https://docs.paperless-ngx.com/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API versioning

Clients choose a version per request so server data model changes do not break them.

## Selecting
```
Accept: application/json; version=10
```
Without it you get the configured default (currently 10). Supported versions are 9 and 10. An invalid version returns `406 Not Acceptable` with an error body.

## Checking compatibility
Make any authenticated request. The response includes:
```
X-Api-Version: 10
X-Version: <server-version>
```
Decide compatibility from the presence or absence of these headers and their values. The docs say to make an authenticated request for this.

## Deprecation policy
Older versions are guaranteed for at least one year after a newer version is released; afterwards support may (but is not guaranteed to) be dropped.

## Version specific behaviour
From version 10, document-editing operations (merge, rotate, edit_pdf) have individual endpoints. Document file versions are a separate concept, handled by `?version={version_id}` and the `update_version` endpoint.

## Checked
2026-11-04. Compared with the API Versioning section of the API page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: Accept header form, default 10, supported 9 and 10, 406 on invalid version, the two response headers, the one-year guarantee, version 10 document-editing endpoints. Removed: "without notice" (the page says support may be dropped, not guaranteed), the unauthenticated-probe inference, and the advice line to pin the version in every integration (not on the page).

Method: documentation only; no commands were run.
