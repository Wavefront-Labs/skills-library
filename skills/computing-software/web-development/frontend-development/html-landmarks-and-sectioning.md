---
id: computing-software.web-development.frontend-development.html-landmarks-and-sectioning
name: html-landmarks-and-sectioning
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, landmark-elements, html-sectioning, landmarks, html, accessibility]
level: practitioner
status: docs-checked
description: "Structuring pages with header, nav, main, aside, footer, section and article so landmarks map correctly for screen readers, with labelling rules and pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/header
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/search
  - https://www.w3.org/WAI/ARIA/apg/practices/landmark-regions/
  - https://www.w3.org/TR/html-aam-1.0/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Landmark and sectioning elements

**Goal:** a screen-reader user can jump between banner, navigation, main, complementary and contentinfo regions, and every region is named when there are several of a kind.

## 1. Element to landmark mapping (HTML-AAM)
| Element | Role | Condition |
|---|---|---|
| `<header>` | banner | only when its context is `body` |
| `<footer>` | contentinfo | only when its context is `body` |
| `<nav>` | navigation | always |
| `<main>` | main | exactly one visible per page |
| `<aside>` | complementary | |
| `<section>` | region | only if it has an accessible name |
| `<search>` | search | |

## 2. Skeleton
```html
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header>…logo…<nav aria-label="Primary">…</nav></header>
  <main id="main">
    <article>
      <h1>…</h1>
      <section aria-labelledby="specs"><h2 id="specs">Specifications</h2>…</section>
    </article>
    <aside aria-label="Related products">…</aside>
  </main>
  <footer><nav aria-label="Footer">…</nav></footer>
</body>
```

## 3. Rules
- All content should live inside some landmark; stray text between landmarks is missed by landmark navigation.
- Two `<nav>`s need distinct labels ("Primary", "Breadcrumb", "Footer").
- `<section>` is not a generic wrapper - use `<div>` when there is no heading/name. `<article>` is for self-contained content (post, card, comment).
- Do not add redundant roles (`<nav role="navigation">`) - harmless but noise.
- Hidden `<main>` elements (SPA views) must use the `hidden` attribute so only one is exposed.

## Verify
- axe rules `region`, `landmark-one-main`, `landmark-unique`, `landmark-no-duplicate-banner` pass.
- A screen reader lists each landmark with its label.

## Checked
2026-10-26. W3C APG landmark regions practice page, MDN header, footer, section and search pages, and axe-core rule descriptions v4.14 (main, 2026-10-26): confirmed aside to complementary, nav to navigation, main to main, section to region only with an accessible name, search to search, header to banner and footer to contentinfo only in the body context, that all content should sit in a landmark, that repeated landmarks need unique labels, and the four axe rule ids. Removed the form row, the role-word-in-label remark, the role=main advice and screen-reader key names.
Method: documentation only; no commands were run.
