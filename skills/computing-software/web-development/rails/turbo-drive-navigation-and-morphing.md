---
id: computing-software.web-development.rails.turbo-drive-navigation-and-morphing
name: turbo-drive-navigation-and-morphing
category: computing-software
field: web-development
product: rails
tags: [turbo-drive, turbo-morphing, turbo-prefetch, data-turbo-track, hotwire, rails]
level: practitioner
status: docs-checked
description: "Turbo Drive in practice: intercepted navigation and forms, form response rules, asset tracking, prefetch, permanent elements, morph refreshes."
sources:
  - https://turbo.hotwired.dev/handbook/drive
  - https://turbo.hotwired.dev/handbook/page_refreshes
  - https://turbo.hotwired.dev/reference/attributes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Turbo Drive navigation and morphing

## 1. What Drive does
Intercepts link clicks and form submissions and renders the next page without a full page reload. A progress bar appears for pages that take longer than 500 ms to load.

## 2. Form response rules
- Success: **redirect**. After a stateful form submission Turbo Drive expects an HTTP 303 redirect, which it follows; in Rails use `redirect_to path, status: :see_other` for non-GET requests.
- Validation failure: render the form with an error status, in Rails `render :new, status: :unprocessable_entity` (see the handbook's form submission section for how Turbo treats non-redirect responses).

## 3. Opting out and controls
```erb
<%= link_to "Download", report_path, data: { turbo: false } %>
<%= button_to "Delete", post_path(@post), method: :delete, data: { turbo_confirm: "Sure?" } %>
<%= link_to "Archive", archive_path, data: { turbo_method: :patch } %>
```
`data-turbo-action="replace"` replaces instead of pushing history.

## 4. JavaScript lifecycle
Page-load JavaScript that runs once per full page load will not re-run on Drive visits; prefer Stimulus controllers (connect/disconnect handle swaps). `data-turbo-permanent` (the element needs a unique `id`) keeps an element across page loads, for example players or chat widgets.

## 5. Assets and caching
```erb
<%= stylesheet_link_tag "application", "data-turbo-track": "reload" %>
```
When a tracked asset changes after a deploy, Turbo performs a full page reload (annotate asset elements with `data-turbo-track="reload"` and include a version identifier in the asset URL). Turbo renders a cached preview on revisits; use `<meta name="turbo-cache-control">` to opt a page out of caching (see the attributes reference).

## 6. Turbo 8 features
- **Prefetch on hover** is on by default; disable globally `<meta name="turbo-prefetch" content="false">` or per link `data-turbo-prefetch="false"` (e.g. links with side effects or heavy pages).
- **Morphing page refreshes**: `<meta name="turbo-refresh-method" content="morph">` and `<meta name="turbo-refresh-scroll" content="preserve">`; redirecting back to the same page morphs the DOM instead of replacing it, with scroll preservation. With `broadcasts_refreshes` on models, all viewers refresh via Action Cable.

## Verify
- [ ] Submitting an invalid form re-renders errors (422); after a CSS deploy, navigating triggers a full reload; widgets survive navigation.

## Checked

2026-10-28. Confirmed from the Turbo Drive handbook (progress bar after 500 ms, 303 redirect expectation after stateful form submissions, `data-turbo-track="reload"` with a versioned URL, cached previews, prefetch on hover enabled since Turbo 8 and `turbo-prefetch` meta, `data-turbo-confirm`), the attributes reference (`data-turbo-action` replace/advance, `data-turbo-permanent` needs a unique id, `turbo-cache-control`, `turbo-refresh-method`, `turbo-refresh-scroll`) and the page refreshes handbook (`broadcasts_refreshes`). Removed (not found): `turbo:load`, the `fetch`/head-merge description, `javascript_importmap_tags`, the "200 is ignored" claim, focus preservation, the `no-cache` meta value.

Method: documentation only; no commands were run.
