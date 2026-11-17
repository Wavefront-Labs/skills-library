---
id: computing-software.web-development.ghost.ghost-content-api-errors
name: ghost-content-api-errors
category: computing-software
field: web-development
product: ghost
tags: [ghost, content-api, errors, http-status, troubleshooting]
level: intro
status: docs-checked
description: "Interpret Ghost Content API error responses: 400, 401, 403, 404 and 500 meanings and the JSON errors array with errorType."
sources:
  - https://github.com/TryGhost/docs/blob/main/content-api/errors.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: diagnose a failing Content API call quickly.

Status codes documented for the Content API:
- 400: badly formed query, for example a filter that is not correctly URL encoded.
- 401: authentication failure, for example an unrecognised key.
- 403: permissions error, for example an under-privileged user.
- 404: unknown resource, including data that is not public.
- 500: server error.

Errors are JSON: an `errors` array of objects. Read `errorType` together with the HTTP status; the `message` field says what went wrong, for example `{"message": "Unknown Content API Key", "errorType": "UnauthorizedError"}`.

Triage steps:
1. 401: re-copy the key from Integrations in Ghost Admin and check you are using the Content key, not the Admin key.
2. 400: URL encode the `filter` value (`+` and `,` are meaningful NQL characters).
3. 404 on a post you know exists: confirm it is published and public, since non-public data returns not found.
4. Check the base URL uses the admin domain and correct protocol.

Verify: a corrected request returns 200 with the expected resource key and no `errors` array.

## Checked

2026-11-04. Confirmed: the five status codes with their examples, the errors array, errorType and message, the example error body (Content API errors page); NQL encoding note (filtering page). Removed: nothing.

Method: documentation only; no commands were run.
