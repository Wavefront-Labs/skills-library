---
id: computing-software.web-development.payload-cms.production-deployment
name: production-deployment
category: computing-software
field: web-development
product: payload-cms
tags: [deployment, production, secure-cookies, security-headers]
level: practitioner
status: docs-checked
description: "Prepare Payload for production: strong secret, tested access control, start script, secure cookies, security headers and file storage."
sources:
  - https://payloadcms.com/docs/production/deployment
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Production deployment checklist

Goal: deploy safely.

Security items from the docs:

- Use a long, complex `secret`.
- Test access control; defaults need a logged-in user, but public registration needs stricter functions.
- Run in production mode: Next.js uses `next start` (TanStack Start serves the built bundle), not the dev server.
- Use TLS and enable secure cookies in your auth collection config.
- Set HTTP security headers yourself (Content-Security-Policy, X-Frame-Options, HSTS); Payload does not because values depend on your embedding and domains. CSP and framing rules can affect custom Admin components and Live Preview.
- Enable the built-in anti-abuse features (login lockout, GraphQL complexity limits, max depth).

Database notes: AWS DocumentDB needs authentication connection options in `connectOptions` passed to `mongooseAdapter`. Azure Cosmos DB is not fully compatible with the MongoDB API: spread `compatibilityOptions.cosmosdb` into the adapter and set `indexSortableFields: true`.

File storage: Heroku and DigitalOcean Apps have ephemeral filesystems, so uploaded files vanish; use a persistent host or an official cloud storage adapter (Azure Blob, Google Cloud Storage, AWS S3, Vercel Blob) instead of local disk on those platforms.

Verify: from outside, `/admin` loads over HTTPS and an anonymous API read of a protected collection is denied.

## Checked

2026-11-04. Read production/deployment. Confirmed: the long complex secret, default access control requiring a logged-in user, running the production start script rather than the dev server, secure cookies with TLS, the HTTP security header guidance (Payload does not set them), the anti-abuse pointer, DocumentDB connectOptions, the Cosmos DB preset and indexSortableFields, and ephemeral filesystems on Heroku and DigitalOcean Apps. Corrected: DigitalOcean App Platform to the page's wording, DocumentDB handling, and removed R2 from the storage list because the page lists Azure, GCS, S3 and Vercel Blob.
Method: documentation only; no commands were run.
