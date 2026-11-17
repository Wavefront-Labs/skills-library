---
id: computing-software.web-development.appwrite.appwrite-rest-api-headers
name: appwrite-rest-api-headers
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, api, rest, headers, authentication]
level: intro
status: docs-checked
description: "Call the Appwrite REST API directly with the project, API key, JWT, fallback-cookie and impersonation headers."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/apis/rest/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use raw HTTP.

Base: your endpoint such as `https://<REGION>.cloud.appwrite.io/v1` plus the route. Every request needs `X-Appwrite-Project: <PROJECT_ID>` and `Content-Type: application/json`.

Authentication options:
- `X-Appwrite-Key: <API_KEY>` for server-side calls with scoped API keys.
- `X-Appwrite-JWT: <JWT>` to act as a user with a JWT.
- Session cookie, or `X-Fallback-Cookies` when third-party cookies are blocked, for client sessions.
- Impersonation headers `X-Appwrite-Impersonate-User-Id`, `-Email` or `-Phone`.

Format: `X-Appwrite-Response-Format` pins the response format version so upgrades do not change shapes.

Queries are sent as JSON-encoded strings in a `queries[]` parameter.

Gotcha: never send the API key from a browser.

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): apis/rest. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed "short-lived" for JWTs, the X-Appwrite-Dev-Key line (not on the REST page), "for operators", the response-codes sentence, the invented Verify and the SDK-for-debugging note; description reworded.

Method: documentation only; no commands were run.
