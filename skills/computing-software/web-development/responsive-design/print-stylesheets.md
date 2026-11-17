---
id: computing-software.web-development.responsive-design.print-stylesheets
name: print-stylesheets
category: computing-software
field: web-development
product: responsive-design
tags: [responsive-components, print-styles, media-print, page-breaks, css]
level: practitioner
status: verified
description: "Writing print stylesheets: @media print resets, hiding chrome, showing link URLs, page breaks with break-inside, @page size and margins, and testing with print emulation."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media#print
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@page
  - https://developer.mozilla.org/en-US/docs/Web/CSS/break-inside
  - https://www.smashingmagazine.com/2018/05/print-stylesheets-in-2018/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Print stylesheets

People print receipts, tickets, invoices, recipes, articles and documentation - and "Save as PDF" uses print styles too.

## 1. Baseline
```css
/* run: Chromium 156 PDF, 2 pages with the break-before page rule, hidden nav/footer absent, link text became "link (https://example.com/x)", #anchor links got no URL */
@media print {
  header nav, footer, .cookie-banner, .chat-widget, .ads, video, .no-print { display: none !important; }
  body { font: 11pt/1.4 Georgia, serif; color: #000; background: #fff; }
  main { width: auto; margin: 0; }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 90%; word-break: break-all; }
  a[href^="#"]::after, a.no-url::after { content: ""; }
  img, svg, figure, table, pre, blockquote { break-inside: avoid; }
  h1, h2, h3 { break-after: avoid; }
  thead { display: table-header-group; }   /* repeat table headers on each page; run: header on all 3 pages, whereas table-row-group printed it once */
  p { orphans: 3; widows: 3; }
}
@page { size: A4; margin: 15mm 12mm; }
@page :first { margin-top: 25mm; }
```

## 2. Details
- Browsers drop backgrounds by default; force where essential (status colours, QR codes): `print-color-adjust: exact;` (Firefox 97, Safari 15.4, Chrome 136 per MDN compat data).
- Dark themes: reset colours in print or users get black pages (or white text on white).
- Lazy-loaded images below the fold may not be loaded when printing in some browsers (Chromium 156 `page.pdf` did load one 3000px down in a run) - use `loading="eager"` for content that must print, or listen to `beforeprint` to swap.
- Fixed headers repeat on every page (run: a `position: fixed` element appeared on all 6 pages of a PDF) or overlap - set `position: static`.
- `break-before: page` for sections that must start a new page (invoices, labels).
- `size: landscape` for wide tables; `@page` margin boxes (headers/footers with page numbers) are only supported in Chromium 131+ for `@top-center` etc. (MDN compat data lists Firefox and Safari as unsupported; run on Chromium 156: `@top-center { content: "HDR-TEXT" }` and `@bottom-right { content: "Page " counter(page) " of " counter(pages) }` rendered "Page 1 of 2").

## 3. Print-specific content
`.print-only { display: none } @media print { .print-only { display: block } }` for things like a printed URL/QR to the page or contact details.

## 4. JS hooks
`window.print()` from a "Print" button; `beforeprint`/`afterprint` events to expand collapsed sections (`details` open) and restore.

## Verify
DevTools > Rendering > Emulate CSS media type: print; print preview in Chrome, Firefox and Safari; save as PDF and check page breaks and URLs.
