---
id: computing-software.web-development.frontend-development.heading-hierarchy-and-outline
name: heading-hierarchy-and-outline
category: computing-software
field: web-development
product: frontend-development
tags: [semantic-html, heading-hierarchy, document-outline, headings, html, accessibility, wcag-1-3-1]
level: practitioner
status: docs-checked
description: "Building a heading hierarchy that screen-reader users can navigate: one h1, no skipped levels, styling decoupled from level, and why the HTML outline algorithm never worked."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements
  - https://www.w3.org/WAI/tutorials/page-structure/headings/
  - https://html.spec.whatwg.org/multipage/sections.html#headings-and-outlines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heading hierarchy and document outline

**Goal:** headings form a table of contents, so the levels must reflect structure.

## 1. Rules
- One `<h1>` describing the page's main content (usually matches the title minus site name).
- Do not skip levels going down (h2 -> h4). Going back up any number is fine.
- Choose the level from structure, the size from CSS: `<h2 class="text-sm">`. Never pick `<h4>` because it "looks right".
- Do not use headings for visual emphasis on non-heading text (taglines, card prices) - use `<p class>`.
- Every landmark section that has a visible title should start with a heading.

## 2. The outline algorithm is dead
Nesting `<h1>` inside `<section>` was supposed to auto-demote levels. MDN notes that nesting several `<h1>` elements in sectioning elements is now non-conforming. Use explicit levels.

## 3. Components and CMS content
- Reusable components should accept a level prop: `<Card headingLevel={3}>` rendering `` `h${level}` ``.
- Rich text from a CMS often starts at h1 or h2 regardless of placement - shift levels on render or restrict the editor's allowed blocks.
- Visually hidden headings (`.visually-hidden`) are acceptable for regions that are visually obvious but unlabelled (e.g. "Filters").

## 4. Visually hidden utility
```css
.visually-hidden{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
```

## Verify
- `document.querySelectorAll("h1,h2,h3,h4,h5,h6")` listed with levels reads like a sensible ToC.
- axe rules `heading-order` and `page-has-heading-one` pass.
- Screen reader heading navigation lists a sensible outline.

## Checked
2026-10-26. MDN heading elements page and axe-core rule descriptions v4.14 (main, 2026-10-26): confirmed do not skip heading levels, prefer a single h1, nested h1 in sectioning elements is non-conforming, and the axe rule ids heading-order and page-has-heading-one. Removed the WebAIM survey statistic, the 2022 spec-removal date, the UA-style claim and screen-reader key names, none of which a fetched source confirms.
Method: documentation only; no commands were run.
