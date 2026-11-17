---
id: computing-software.web-development.frontend-development.open-graph-and-social-cards
name: open-graph-and-social-cards
category: computing-software
field: web-development
product: frontend-development
tags: [open-graph-meta, twitter-card-meta, og-image, social-sharing, link-previews, html, seo]
level: practitioner
status: docs-checked
description: "Open Graph meta tags so shared links render a title, description and image: the four required properties, optional image properties, server-rendered tags and scraper checks."
sources:
  - https://ogp.me/
  - https://developers.facebook.com/docs/sharing/webmasters/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Open Graph and social cards

**Goal:** every shareable URL produces a correct preview in Slack, iMessage, LinkedIn, Facebook, X, Discord.

## 1. Minimum tag set
```html
<meta property="og:type" content="article">
<meta property="og:title" content="How we cut LCP by 40%">
<meta property="og:description" content="One to two sentence summary.">
<meta property="og:url" content="https://example.com/blog/lcp">
<meta property="og:image" content="https://example.com/og/lcp.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Chart showing LCP falling from 3.1s to 1.8s">
<meta property="og:site_name" content="Example">
```
- The four required properties for every page are `og:title`, `og:type`, `og:image` and `og:url`; `og:description` and `og:site_name` are optional. Per the protocol, `og:image` also takes optional `og:image:width`, `og:image:height`, `og:image:type`, `og:image:secure_url` and `og:image:alt` (specify `og:image:alt` whenever you specify `og:image`).
- Use absolute URLs (scheme + host) for `og:image` and `og:url`.
- `og:url` is the canonical URL of the object, used as its permanent ID in the graph.

## 2. Image rules
- Declare `og:image:width` and `og:image:height` to match the real image; check each platform's current image size guidance in its own docs.
- The image must be publicly fetchable without cookies.

## 3. SPAs and frameworks
The protocol puts the tags in the `<head>` of the page; put them in the server-rendered HTML rather than adding them client-side, and check with a raw `curl` of the page.

## 4. Gotchas
- Platforms cache previews; use each platform's own debugger to force a re-scrape after changing tags.
- Bots can be blocked by WAF/bot rules; allowlist the scraper user agents you need.
- Login walls stop previews.

## Verify
- [ ] `curl -A facebookexternalhit/1.1 https://example.com/page | grep og:` shows tags in raw HTML.
- [ ] Platform debuggers show no warnings.
- [ ] Image URL returns 200 with an image content type to an anonymous request.

## Checked
2026-10-31. Confirmed against ogp.me: the four required properties, og:description and og:site_name, og:image optional structured properties including og:image:alt, og:url as canonical permanent ID, tags in head. Removed: X/Twitter card claims (source page unreadable), image size and file-size limits, per-platform cache timings, bot names, framework metadata APIs.
Method: documentation only; no commands were run.
