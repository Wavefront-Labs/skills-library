---
id: computing-software.web-development.web-accessibility.page-titles-and-spa-title-updates
name: page-titles-and-spa-title-updates
category: computing-software
field: web-development
product: web-accessibility
tags: [navigable, wcag-navigable, page-title, wcag-2-4-2, document-title, spa-accessibility, route-change]
level: practitioner
status: verified
description: "Meeting WCAG 2.4.2 Page Titled: unique descriptive title patterns, updating document.title on SPA route changes and states like errors or search results."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html
  - https://www.w3.org/WAI/WCAG22/Techniques/general/G88
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page titles and SPA title updates

**Goal:** every view has a unique `<title>` that tells users where they are - it's the first thing screen readers announce and what tabs/history show.

## 1. Pattern
`<specific page> - <section> - <site>`, most specific first:
- `Edit invoice INV-1042 - Invoices - Acme`
- `Search results for "red shoes" (24) - Acme`
- `Error: Checkout - Acme` when the form has errors (GOV.UK Design System error summary guidance: add "Error: " to the start of the page title)
- Step flows: `Payment (step 3 of 4) - Checkout - Acme`
Avoid identical titles across pages and titles that are just the site name or a URL.

## 2. SPAs must update it
Client-side routing doesn't change the title automatically.
- React Router / custom: set `document.title` in a route effect, or use React 19 `<title>` in components (hoisted to head).
- Next.js App Router: `export const metadata = { title }` / `generateMetadata`; template `{ title: { template: '%s - Acme', default: 'Acme' } }` in the root layout.
- Vue Router (an earlier escaped-backtick version of this line was a syntax error; this one parses):
  ```js
  router.afterEach(to => { document.title = to.meta.title ? `${to.meta.title} - Acme` : 'Acme' })
  ```
  Nuxt: `useHead`/`useSeoMeta`.
- Update when content-defining state changes (search query, item loaded), not just on route change; set a loading title then the real one.

## 3. Pair with focus/announcement
Changing the title isn't announced by most screen readers on SPA navigation. Also move focus to the main heading or announce the new page (see SPA route-change skill).

## 4. Iframes
`<iframe title="Payment form">` - frames need titles too (4.1.2).

## Verify
- [ ] Crawl/list all routes: titles unique and descriptive (a script comparing `document.title` per route).
- [ ] Navigating in the SPA updates the tab title every time, including back/forward.
- [ ] Error state titles start with "Error:".
