---
id: computing-software.web-development.frontend-development.html-head-metadata
name: html-head-metadata
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, html-head-metadata, meta-viewport, canonical-url, meta-description, charset, open-graph, html]
level: practitioner
status: docs-checked
description: "Writing a correct HTML head: charset first, viewport, title, meta description, canonical, social cards, icons, and the order and mistakes that break them."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/head
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/base
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTML head metadata

**Goal:** every page parses with the right encoding, scales correctly on phones, has a unique title/description, and declares one canonical URL.

## 1. Baseline template
```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">                         <!-- within the first 1024 bytes -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Order history – Acme</title>              <!-- page-specific first, site name last -->
  <meta name="description" content="View, track and return your Acme orders.">
  <link rel="canonical" href="https://www.acme.com/orders">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <meta property="og:title" content="Order history">
  <meta property="og:image" content="https://www.acme.com/og/orders.png"> <!-- absolute URL -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0b5fff">
</head>
```

## 2. Rules that matter
- A `<meta>` that declares the character encoding must sit entirely within the first 1024 bytes of the document, so put it first in `<head>`.
- Viewport: never add `maximum-scale=1` or `user-scalable=no` - MDN warns that disabling zoom stops people with low vision reading the page, and WCAG 1.4.4 (Resize Text) applies.
- One `<title>` per page, unique. SPAs must update `document.title` on route change.
- Give each page its own meta description.
- `rel="canonical"` names the preferred URL for the document (MDN rel values table); use an absolute URL.
- `<base href>` sets the base URL for all relative URLs in the document and only one is allowed; avoid unless required.

## 3. Ordering for performance
Put the charset declaration first (see above); keep the remaining order consistent across pages.

## Verify
- View source (not DevTools Elements) - the server HTML must contain these tags; crawlers and link unfurlers often do not run JS.
- `document.characterSet === "UTF-8"`.
- Paste the URL into a social card validator and check the preview image.

## Checked
2026-10-26. MDN meta, base, viewport and rel pages (main, 2026-10-26): confirmed the charset declaration must be within the first 1024 bytes, viewport zoom-disabling is discouraged for low-vision users and WCAG 1.4.4, base sets the URL for all relative URLs with one allowed per document, and canonical is a documented rel value for the preferred URL. Removed search-engine specifics (title and description lengths, ranking, pagination canonicals), the 1200x630 and 180x180 sizes, the head ordering advice and the Lighthouse audit names, which no fetched documentation confirms.
Method: documentation only; no commands were run.
