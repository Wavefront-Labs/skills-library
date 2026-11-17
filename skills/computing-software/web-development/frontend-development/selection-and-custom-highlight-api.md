---
id: computing-software.web-development.frontend-development.selection-and-custom-highlight-api
name: selection-and-custom-highlight-api
category: computing-software
field: web-development
product: frontend-development
tags: [custom-highlight-api, selection-pseudo-element, highlight-pseudo, text-highlighting, css-selectors]
level: advanced
status: docs-checked
description: "Styling text selection with ::selection and highlighting ranges without DOM changes using the CSS Custom Highlight API: search hits, spellcheck marks, priorities and limits."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::selection
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::highlight
  - https://www.w3.org/TR/css-highlight-api-1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ::selection and the CSS Custom Highlight API

## 1. ::selection
```css
::selection { background: color-mix(in oklch, var(--accent) 35%, transparent); color: inherit; }
.code ::selection { background: #264f78; }
```
Only `color`, `background-color`, `text-decoration` (and its associated properties), `text-shadow`, and `-webkit-text-stroke-color`, `-webkit-text-fill-color` and `-webkit-text-stroke-width` apply. Keep selected text readable: MDN cites WCAG contrast of 4.5:1 for text (3:1 for large text) between the selected text and the selection background. Don't set `user-select: none` on content people may want to copy.

## 2. Custom Highlight API (Chrome 105, Safari 17.2, Firefox 140)
Highlights arbitrary `Range`s without wrapping text in `<mark>` spans - no DOM mutation, no broken event listeners or React reconciliation.
```js
function highlightMatches(root, query) {
  CSS.highlights.delete("search");
  if (!query) return;
  const ranges = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const q = query.toLowerCase();
  for (let n; (n = walker.nextNode()); ) {
    const text = n.data.toLowerCase();
    for (let i = text.indexOf(q); i !== -1; i = text.indexOf(q, i + q.length)) {
      const r = new Range(); r.setStart(n, i); r.setEnd(n, i + q.length); ranges.push(r);
    }
  }
  CSS.highlights.set("search", new Highlight(...ranges));
}
```
```css
::highlight(search) { background: yellow; color: black; }
::highlight(current) { background: orange; }
```

## 3. Details
- `highlight.priority = 1` orders overlapping highlights: a higher priority is above in the stacking order, and with equal priority the most recently registered highlight wins. Use one highlight name per highlight (the spec advises against several names).
- Ranges are live: editing the text node updates or collapses them; re-run after content changes.
- Only the same limited property set as `::selection` applies to `::highlight()`; no layout changes, no `padding`.
- The specification says user agents should expose custom highlights to assistive technology and uses `highlight.type` (`"highlight"`, `"spelling-error"`, `"grammar-error"`) to convey meaning, but do not rely on it: if the highlight matters (current search hit), also announce it ("3 of 12 matches") via a live region and scroll the current range into view.
- Matches don't cross element boundaries in this simple walker; join text nodes for phrases spanning `<em>`.

## 4. Uses
Find-in-page for virtualised docs, syntax highlighting without spans (big perf win on large code blocks), collaborative cursors/comments, spellcheck-style underlines with `::highlight(err) { text-decoration: wavy underline red; }`.

## Verify
- [ ] Highlights clear and recompute on query change; no DOM nodes added; current match announced to screen readers; selection colours meet contrast.

## Checked

Checked 2026-10-26 against mdn/content (main) `::selection`, `::highlight()` and CSS Custom Highlight API pages, the CSS Custom Highlight API Module Level 1 draft (w3c/csswg-drafts) and mdn/browser-compat-data.

- Fixed: the contrast advice said 3:1; MDN cites 4.5:1 for text (3:1 for large text). The note "not exposed to assistive technology" is replaced by the draft's wording (user agents should expose highlights; `type` carries the meaning).
- Fixed: "Baseline 2025" removed; versions are Chrome 105, Safari 17.2, Firefox 140. Priority rule: higher priority is above, ties go to the most recently registered highlight.
- Confirmed: the allowed property list for `::selection` and `::highlight()`; `CSS.highlights` registry; ranges are live ranges adjusted by the user agent on DOM changes.

Method: documentation only; no commands were run.
