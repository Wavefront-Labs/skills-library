---
id: computing-software.web-development.web-accessibility.bypass-blocks-and-skip-links
name: bypass-blocks-and-skip-links
category: computing-software
field: web-development
product: web-accessibility
tags: [bypass-blocks, skip-links, wcag-2-4-1, landmarks, screen-reader-navigation]
level: intro
status: verified
description: "Meeting WCAG 2.4.1 Bypass Blocks: skip links that work, landmark regions and headings for screen reader navigation, skip links in SPAs, and testing with keyboard and rotor."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/bypass-blocks.html
  - https://webaim.org/techniques/skipnav/
  - https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bypass blocks: skip links and landmarks

2.4.1 (A): a mechanism to skip blocks of content repeated on multiple pages (header, navigation). Landmarks satisfy it for screen-reader users; a skip link is needed for sighted keyboard users, who have no landmark navigation by default.

## 1. Skip link
```html
<body>
  <a class="skip-link" href="#main">Skip to main content</a>
  <header>...</header><nav>...</nav>
  <main id="main" tabindex="-1">...</main>
```
```css
.skip-link { position: absolute; left: 1rem; top: -100px; z-index: 1000; padding: .75rem 1rem; background: #000; color: #fff; }
.skip-link:focus { top: 1rem; }
main:focus { outline: none; }   /* programmatic focus target; don't show a giant ring */
```
- First focusable element on the page; visible when focused (never `display: none`). Run in Chromium: first Tab focused the skip link, Enter moved focus to `main[tabindex=-1]`, and the next Tab reached the first button inside main.
- `tabindex="-1"` on the target makes focus actually move there in all browsers, so the next Tab continues inside main.
- Target must exist on every template; broken `#main` links are a common audit finding.
- Optional extra links ("Skip to search", "Skip to results") on complex pages; keep it short.

## 2. Landmarks and headings
- One `<main>`, `<header>` (banner), `<nav>` with `aria-label` when there are several, `<footer>` (contentinfo), `<aside>`, `<search>`.
- All content inside some landmark (axe rule `region`).
- A logical heading structure with an `<h1>` at the start of main content - many screen-reader users navigate by headings first.

## 3. SPAs
Client routing doesn't reset focus: after navigation move focus to the new page's `<h1>` or main (with `tabindex="-1"`) and update `document.title`, so the skip link and screen readers start at the new content.

## 4. Sticky headers
Ensure the skip target isn't hidden under a sticky header (`scroll-margin-top`) - WCAG 2.4.11 Focus Not Obscured.

## Verify
- [ ] First Tab shows "Skip to main content"; Enter then Tab lands on the first focusable item in main; screen reader landmarks list shows banner, navigation, main, contentinfo.
