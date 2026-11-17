---
id: computing-software.general-digital-literacy.office-suites.headings-reading-order-and-table-headers
name: headings-reading-order-and-table-headers
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, reading-order, table-headers, selection-pane, header-row, meaningful-link-text, document-structure]
level: intro
status: docs-checked
description: "Make documents and slides navigable by assistive tech: real headings, correct slide reading order, table header rows and meaningful link text."
sources:
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker
  - https://www.w3.org/WAI/fundamentals/accessibility-intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Headings, reading order and table headers

**Goal:** screen-reader users can navigate the document the same way sighted readers skim it.

## Documents
- Use the built-in heading styles in order; the Accessibility Checker gives a Tip for missing heading styles. Use real list and column features, not typed dashes or spaces.

## Slides: reading order
- **Windows:** use the Accessibility Checker and its **Reading Order** pane; screen readers read objects in the order listed in that pane.
- **Mac:** **Home > Arrange > Selection Pane**, drag items to reorder. Microsoft's page says screen readers read in the reverse of the order listed there, and the Windows and Mac sections differ, so test with a screen reader.
- Every slide needs a unique, descriptive **title**, even if it is not visible; a title can be positioned off the slide. A missing slide title is an Error; the reading-order check is a Warning.

## Tables
- Mark the first row as a header: in PowerPoint, Table Design tab > **Header Row** checkbox (Table Style Options group).
- Avoid split cells, merged cells and nested tables (a checker Warning).

## Verify
- [ ] Heading list shows all headings; each slide's title is read first in the Reading Order pane.

## Checked

2026-10-27. Microsoft Support 'Make your PowerPoint presentations accessible' and Accessibility Checker rules pages (read 2026-10-27): Reading Order pane vs Selection Pane direction (the page itself notes the Windows/Mac difference), titles, Header Row path, rule severities. Removed: the claim that objects read bottom to top on Windows, Word/Excel header-row and Google Slides steps, no-blank-row and Word Edit Link advice (not confirmed).

Method: documentation only; no commands were run.
