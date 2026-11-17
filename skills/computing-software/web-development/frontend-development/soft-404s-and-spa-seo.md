---
id: computing-software.web-development.frontend-development.soft-404s-and-spa-seo
name: soft-404s-and-spa-seo
category: computing-software
field: web-development
product: frontend-development
tags: [soft-404, spa-seo, http-status-codes, noindex, javascript-seo, client-side-routing]
level: practitioner
status: docs-checked
description: "Avoiding soft 404s in client-rendered apps: real status codes via SSR, noindex or redirect strategies for CSR, unique titles/canonicals, and checking Search Console."
sources:
  - https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics#use-meaningful-http-status-codes
  - https://developers.google.com/search/docs/crawling-indexing/http-network-errors#soft-404-errors
  - https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Soft 404s and SPA SEO

A soft 404 is a page that says "not found" (or is nearly empty) but returns HTTP 200. SPAs with an `index.html` fallback produce them for every bad URL and every deleted item.

## 1. Best fix: decide the status on the server
With SSR/SSG (your framework's not-found response, or a server-rendered view) the server returns a real 404/410 with the not-found UI.

## 2. Pure CSR options (Google's guidance)
- Redirect to a URL the server answers with 404: `window.location.href = "/not-found"` where the server returns status 404 for `/not-found`.
- Or add noindex from JS on the error view:
```js
const m = document.createElement("meta"); m.name = "robots"; m.content = "noindex"; document.head.append(m);
```
This is one of the two strategies Google documents for client-rendered apps.

## 3. Other SPA SEO basics
- Unique `<title>`, meta description and canonical per route, updated on navigation (and server-rendered where possible).
- Real `<a href>` links: Googlebot discovers URLs from href attributes.
- Do not disallow in robots.txt the URLs a page needs to render; Googlebot skips URLs robots.txt disallows.

## Verify
- [ ] `curl -I https://site/doesnotexist` -> 404 (SSR) or the page sets noindex after render.
- [ ] Search Console reports fewer soft 404s after the fix.

## Checked
2026-10-28 Confirmed on Google Search Central (JavaScript SEO basics, fix-search-javascript): soft 404 avoidance in client-side apps by redirecting to a URL that returns 404 or adding a robots noindex meta tag; Googlebot checks robots.txt before fetching and reads href attributes. Removed: framework-specific not-found calls, 410/301 advice, crawler-behaviour claims, IntersectionObserver and fragment claims, Search Console menu names.
Method: documentation only; no commands were run.
