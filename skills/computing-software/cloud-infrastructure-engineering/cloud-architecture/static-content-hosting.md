---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.static-content-hosting
name: static-content-hosting
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-patterns, static-content-hosting, static-website, object-storage, cdn, origin-access-control, cache-control, immutable-assets]
level: practitioner
status: docs-checked
description: "Serve static assets from object storage behind a CDN: private origin access with CloudFront OAC, SAS for private files, Cache-Control for hashed vs HTML files, deploy ordering."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/static-content-hosting", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html", "https://developer.mozilla.org/docs/Web/HTTP/Headers/Cache-Control"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static content hosting

Deploy static content (HTML, images, CSS, JavaScript, PDFs, packages) to a storage service that
delivers it directly to clients, freeing compute for dynamic requests (Azure pattern page).

## Steps
1. **Endpoint**: expose HTTPS from storage, a CDN or a reverse proxy. A CDN caches near clients;
   benefit depends on client locations, request patterns and hit rates.
2. **Private origin on AWS**: use CloudFront origin access control (OAC), recommended over legacy
   OAI (OAC supports all regions, SSE-KMS and PUT/DELETE). Grant the `cloudfront.amazonaws.com`
   service principal in the bucket policy with a condition on the distribution ARN. Choose
   "Sign requests" so CloudFront always signs origin requests over HTTPS. Set Object Ownership to
   Bucket owner enforced. An S3 website endpoint cannot use OAC or OAI. For SSE-KMS add the
   distribution to the KMS key policy.
3. **Private files on Azure**: the Blob static website endpoint has no authentication, and
   changing the `$web` access level does not make it private. Keep private content in a separate
   private container, authorise the client, then issue a short-lived read-only user delegation SAS;
   treat SAS tokens as credentials and send them only over HTTPS. The static website endpoint does
   not support Azure Storage CORS rules.
4. **Headers**: set `Content-Type`, `Content-Encoding` and `Cache-Control` at deploy time.
   Hashed or versioned assets: `Cache-Control: public, max-age=31536000, immutable`. The HTML that
   references them: `Cache-Control: no-cache` (stored, but revalidated before each reuse). `no-cache`
   does not mean do not store; `no-store` does.
5. **Deploy order**: publish changed assets at new versioned URLs before deploying pages that
   reference them; retain older assets while cached pages or rollback need them.
6. **Invalidation**: changing or deleting origin content does not invalidate cached copies. CDN
   purges do not clear browser caches and take time to propagate.
7. **Redundancy and cost**: pick storage redundancy for zone vs regional outage; cross-region
   replication can be asynchronous. Compare storage and delivery cost to compute you can avoid.
8. **Origins**: restrict direct origin access when it would bypass CDN controls. Allow anonymous
   read only for content meant to be public.

## Not suited
Content personalised per request, or very small volumes where the separate fetch outweighs savings.

## Verify
- [ ] Direct bucket URL is denied; only the CDN reads it.
- [ ] Hashed assets and HTML carry different Cache-Control values.

## Checked
Confirmed against the three cited pages. Removed as not stated there: SPA routing and error-page
rewrites, rollback tooling, content-hashing tool advice and the spa-hosting tag.
Method: docs-only read of cited pages, 2026-11-08
