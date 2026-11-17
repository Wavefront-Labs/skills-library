---
id: computing-software.web-development.directus.api-error-handling
name: api-error-handling
category: computing-software
field: web-development
product: directus
tags: [api-errors, error-codes, forbidden-not-404, token-expired]
level: practitioner
status: docs-checked
description: "Handle Directus API errors by reading errors[].extensions.code, mapping common codes to HTTP statuses and refreshing on TOKEN_EXPIRED."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/5.errors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Responses use one JSON shape; branch on the `code`, not the message:

```json
{ "errors": [ { "message": "You don't have permission to access this.", "extensions": { "code": "FORBIDDEN" } } ] }
```

A response may hold several errors; `extensions` may add context (collection, field, value); development mode adds a `stack`. GraphQL puts the code at `extensions.code` of each error.

Common codes: `FORBIDDEN` 403, `INVALID_CREDENTIALS` 401, `TOKEN_EXPIRED` 401 (refresh it), `INVALID_TOKEN` 403, `INVALID_OTP` 401, `INVALID_IP` 401, `USER_SUSPENDED` 401, `FAILED_VALIDATION` 400, `RECORD_NOT_UNIQUE` 400, `INVALID_QUERY` 400, `REQUESTS_EXCEEDED` 429, `COLLECTION_INACTIVE` 403.

```js
const body = await response.json();
if (!response.ok) {
  const code = body.errors?.[0]?.extensions?.code;
  if (code === 'TOKEN_EXPIRED') { /* refresh and retry */ }
}
```

Gotchas:
- Actions on non-existing items return `FORBIDDEN`, not 404, so item existence is not revealed.
- Extensions and flows can emit other codes; keep a generic fallback.
- Non-admin users get a generic message on 500.

## Checked

2026-11-04: error response shape, multiple errors, extensions context and stack in development mode, GraphQL code location, every listed code with its status, the FORBIDDEN-not-404 rule and the generic fallback note confirmed against the Directus Errors page.

Method: documentation only; no commands were run.
