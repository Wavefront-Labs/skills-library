---
id: computing-software.cloud-infrastructure-engineering.aws.cloudfront-custom-error-responses-and-spa-routing
name: cloudfront-custom-error-responses-and-spa-routing
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloudfront, custom-error-responses, spa-routing, error-caching-ttl, s3-origin, cloudfront-functions]
level: practitioner
status: docs-checked
description: "Configure CloudFront custom error responses and error caching TTLs, and route single-page-app deep links to index.html without masking real API errors."
sources: ["https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GeneratingCustomErrorResponses.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/custom-error-pages-procedure.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/custom-error-pages-expiration.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/custom-error-pages-different-locations.html", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/example_cloudfront_functions_url_rewrite_single_page_apps_section.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CloudFront custom error responses and SPA routing

## 1. Custom error responses
Per distribution, per HTTP error code (the guide lists the 4xx and 5xx codes CloudFront caches; 416 is not cached):
- **Error caching minimum TTL** (default 10 s): how long CloudFront caches the error
  before asking the origin again.
- **Response page path**: an object path (e.g. `/errors/404.html`) served instead of the
  origin's error body; a cache behaviour whose path pattern matches it must route to the origin that holds the pages. Store error pages in a different location from your site (for example an S3 bucket behind a `/errors/*` behaviour); CloudFront needs permission to read them (public, or OAC for S3). If the custom page is unavailable, CloudFront returns the status it got from the origin that holds the error pages.
- **Response code**: optionally change the status (e.g. serve 404 page with 404, or
  200 for SPA fallback).
```json
"CustomErrorResponses": {"Quantity": 2, "Items": [
  {"ErrorCode": 503, "ResponsePagePath": "/errors/maintenance.html", "ResponseCode": "503", "ErrorCachingMinTTL": 5},
  {"ErrorCode": 404, "ResponsePagePath": "/errors/404.html", "ResponseCode": "404", "ErrorCachingMinTTL": 60}]}
```
Lower `ErrorCachingMinTTL` for 5xx so recovery is visible fast. If the origin adds `Cache-Control: max-age` or `s-maxage`, or `Expires`, CloudFront caches the error for the greater of that value and the minimum TTL.

## 2. SPA deep links: two approaches
A React/Vue/Angular app served from S3 has only `/index.html`; a request for `/orders/42`
can return an error (403 or 404 depending on bucket permissions).

**Approach A: custom error response** (simple, common)
Map 403 and 404 to `/index.html` with response code 200. Problem: it applies to the
**whole distribution**, including `/api/*` behaviours, so a genuine API 404 or 403 becomes
a 200 HTML page and clients break in confusing ways.

**Approach B: CloudFront Function URL rewrite** on the static behaviour only (better; illustrative code, AWS's published example for this task instead appends `index.html` to extensionless URLs)
```javascript
function handler(event) {
  var req = event.request;
  var uri = req.uri;
  // anything without a file extension is an app route
  if (!uri.includes('.', uri.lastIndexOf('/'))) {
    req.uri = '/index.html';
  }
  return req;
}
```
Associate as **viewer request** on the default (S3) behaviour; `/api/*` behaviour has no
function, so API errors pass through untouched. Origin sees `/index.html`, status stays 200
naturally, and real missing assets (`/app.js` typo) still 404.

## 3. Caching index.html
- Serve `index.html` with `Cache-Control: no-cache` (or short TTL) and hashed asset files
  (`main.3f2a.js`) with `max-age=31536000, immutable`; then deploys need no invalidation
  except `/index.html`.
- With approach B every app route caches as the same object key `/index.html` (the cache
  key is the rewritten URI), which is efficient.

## 4. Error pages when the origin is down
If custom error pages live on the same origin as the application and it starts returning 5xx, CloudFront cannot fetch them. Keep them in a separate location, as in section 1.

## Gotchas
- A custom error response applies to the whole distribution for that error code, which is why approach A also rewrites genuine API errors.
- Test any 403 mapping against your WAF configuration before relying on it.

## Verify
- [ ] `curl -sI https://app.example.com/orders/42` returns 200 with HTML; `curl -sI https://app.example.com/api/nope` returns the API's real 404 JSON.
- [ ] `curl -sI https://app.example.com/missing.js` returns 404.
- [ ] Stopping the origin shows the custom maintenance page within the 5xx error TTL.

## Checked
2026-10-27. Documentation: Amazon CloudFront Developer Guide (generate custom error responses, configure error response behavior, control how long CloudFront caches errors, store error pages in different locations, CloudFront Functions SPA example), read this date. Confirmed: default 10 s error caching, greater-of rule for Cache-Control and minimum TTL, 416 not cached, separate storage and behaviour path pattern requirement, fallback status when the error page is missing. Confirmed from the CloudFront API model: CustomErrorResponse fields. Removed the unconfirmed error-code list, S3 website endpoint, WAF-interaction and deploy-time claims.
Method: documentation only; no commands were run.
