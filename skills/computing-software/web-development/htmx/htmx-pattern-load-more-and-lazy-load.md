---
id: computing-software.web-development.htmx.htmx-pattern-load-more-and-lazy-load
name: htmx-pattern-load-more-and-lazy-load
category: computing-software
field: web-development
product: htmx
tags: [htmx, pagination, infinite-scroll, lazy-loading, revealed, intersect, click-to-load]
level: practitioner
status: docs-checked
description: "Paginate and defer content with htmx: click-to-load rows, infinite scroll on revealed, and lazy-load a fragment on load, each by swapping the trigger element."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/click-to-load.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/infinite-scroll.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/lazy-load.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: load more data, or defer an expensive fragment, by making the last element of the page carry the request for the next piece.

Click to load. The final table row holds a button; it replaces its whole row with the next page, and that page ends with a new button row for page 3, and so on:

```html
<tr id="replaceMe">
  <td colspan="3">
    <button class="btn primary" hx-get="/contacts/?page=2"
            hx-target="#replaceMe" hx-swap="outerHTML">
      Load More Agents... <img class="htmx-indicator" src="/img/bars.svg" alt="">
    </button>
  </td>
</tr>
```

Infinite scroll. Put the trigger on the last real row instead and append the result after it:

```html
<tr hx-get="/contacts/?page=2" hx-trigger="revealed" hx-swap="afterend">
  <td>Agent Smith</td><td>void29@null.org</td><td>55F49448C0</td>
</tr>
```

`revealed` fires when the element is scrolled into the viewport. If the scroll happens inside a container with CSS `overflow` (such as `overflow-y: scroll`), use `intersect once` instead of `revealed`. The last element of each result carries the listener for the next page.

Lazy load. Fire on `load` and show a placeholder indicator while waiting:

```html
<div hx-get="/graph" hx-trigger="load">
  <img alt="Result loading..." class="htmx-indicator" width="150" src="/img/bars.svg"/>
</div>
```

Fade the arriving content in with the settle phase:

```css
.htmx-settling img { opacity: 0; }
img { transition: opacity 300ms ease-in; }
```

Gotcha: click-to-load swaps `outerHTML` (the button row is replaced), infinite scroll swaps `afterend` (the data row stays and results are appended after it).

## Checked

2026-11-07. Confirmed against the htmx Click to Load, Infinite Scroll and Lazy Loading example pages (all three code samples, `revealed` note and `intersect once` for `overflow`, settling CSS). Removed the unsourced claim about how to stop on the last page and the invented Verify step.
Method: documentation only; no commands were run.
