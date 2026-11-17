---
id: computing-software.web-development.ghost.ghost-api-versioning-accept-version
name: ghost-api-versioning-accept-version
category: computing-software
field: web-development
product: ghost
tags: [ghost, api-versioning, accept-version, content-version, stability]
level: practitioner
status: docs-checked
description: "Use the Accept-Version header and Content-Version response to keep Ghost API clients compatible across major versions."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/api-versioning.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make an API client fail loudly, not silently, when Ghost changes.

Stability index used in the docs: Stable (forward compatible changes only), Experimental (may receive breaking changes), Deprecated (scheduled for removal).

Mechanism:
1. Send `Accept-Version: v{major}.{minor}` on every request. It states the minimum Ghost version your client can operate with.
2. Ghost replies with a `Content-Version` header giving the version of the install that answered.
3. If Ghost receives an Accept-Version header and the request cannot be processed, Ghost emails the site owner and administrators the details, which makes outdated clients easy to find.

Ghost major versions ship every 8-12 months according to this page, so code written against the API today should remain stable for a minimum of two years.

Practice:
- Pin the version in the client constructor (the JavaScript clients take a `version` option).
- Log the `Content-Version` header in integration tests.
- When a major upgrade is planned, bump the pinned version deliberately.

Verify: a response includes `Content-Version`, and your pinned minimum is not higher than it.

## Checked

2026-11-04. Confirmed: stability index, Accept-Version and Content-Version, owner email on failure, 8-12 month major cadence and two-year stability (API versioning page). Removed: the "breaking changes page" pointer and the over-specific wording of the email trigger.

Method: documentation only; no commands were run.
