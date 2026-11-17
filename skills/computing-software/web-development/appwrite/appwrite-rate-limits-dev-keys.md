---
id: computing-software.web-development.appwrite.appwrite-rate-limits-dev-keys
name: appwrite-rate-limits-dev-keys
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, security, rate-limits, dev-keys, abuse-protection]
level: practitioner
status: docs-checked
description: "Read rate limit headers, understand which callers are limited, and handle testing friction including the deprecated dev keys."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/rate-limits/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/dev-keys/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/advanced/security/abuse-protection/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stay within Appwrite rate limits and test without lockouts.

Facts:
- Some endpoints have rate limits to blunt brute force and abuse; each route's reference page lists its limit.
- Limits apply to Client SDKs only. Server SDKs authenticated with an API key are not limited.
- Response headers: `X-RateLimit-Limit` (max requests per hour), `X-RateLimit-Remaining`, and `X-RateLimit-Reset` (UTC epoch seconds). Exceeding the limit returns a 429 error response.
- Extra service-abuse limits may apply to behaviors like rapid content creation, aggressive polling instead of webhooks, high concurrency, or repeatedly requesting expensive data.

Dev keys: secrets sent in the `X-Appwrite-Dev-Key` header by client apps in development to bypass rate limits and CORS errors, with 1, 7 or 30 day expiry. The docs say creation of new dev keys is paused and that dev keys will be deprecated on September 1, 2026; a successful login now resets the login rate limit, so auth testing no longer needs one. Never ship a dev key in production.

Also related: CORS rejects requests from domains not added as a platform (Overview > Platforms).

## Checked

Date: 2026-11-07. Read in full on the appwrite/website docs source (Markdoc): advanced/security/rate-limits, advanced/security/dev-keys, advanced/security/abuse-protection. Code tabs for non-JavaScript SDKs were collapsed when read and Markdoc partials (shared include files) were not opened; all prose and the JavaScript examples were read. Corrections: Removed the SSR single-IP gotcha and the invented Verify; dev-key deprecation worded as the page states (will be deprecated on September 1, 2026); added that exceeding the limit returns 429.

Method: documentation only; no commands were run.
