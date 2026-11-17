---
id: computing-software.web-development.payload-cms.preventing-api-abuse
name: preventing-api-abuse
category: computing-software
field: web-development
product: payload-cms
tags: [api-abuse, rate-limits, graphql-complexity, malicious-uploads]
level: advanced
status: docs-checked
description: "Harden a Payload API: login lockout, depth limits, CSRF, CORS, GraphQL complexity limits and upload scanning."
sources:
  - https://payloadcms.com/docs/production/preventing-abuse
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Preventing API abuse

Goal: apply the built-in anti-abuse controls.

- Failed logins: set `maxLoginAttempts` low and `lockTime` (milliseconds) on auth collections.
- Depth: set the root `maxDepth` (default 10, keep it as small as your app allows) so queries cannot populate deeply or circularly.
- CSRF: configure the root `csrf` allowlist.
- CORS: set `cors` to the exact origins allowed to call the API.
- GraphQL: set `graphQL.maxComplexity` (each field costs 1; relationship and upload fields cost 10). If you do not use GraphQL set `graphQL.disable: true`.
- Uploads: Payload does not execute uploaded files, but malicious files can be stored and served. Enable email verification for registration, keep `create` and `update` access on upload collections tight, limit `read` access, and scan files in a hook (for example with ClamAV) or with antivirus.

```ts
export default buildConfig({
  maxDepth: 3,
  csrf: ['https://my-app.com'],
  cors: ['https://my-app.com'],
  graphQL: { maxComplexity: 500 },
})
```

Verify: a query with a high depth is clamped and a deep GraphQL query is rejected.

## Checked

2026-11-04. Read production/preventing-abuse. Confirmed: maxLoginAttempts and lockTime in milliseconds on auth collections, root maxDepth defaulting to 10, the CSRF and CORS configuration pointers, graphQL.maxComplexity with field cost 1 and relationship and upload cost 10, graphQL.disable: true, and the malicious-upload advice (email verification, strict create, update and read access, ClamAV or antivirus scanning in a hook). The example values 3 and 500 are illustrative, not from the page.
Method: documentation only; no commands were run.
