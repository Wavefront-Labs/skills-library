---
id: creative-arts.graphic-design.adobe-indesign.accessible-tagged-pdf
name: accessible-tagged-pdf
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, accessible-pdf, pdf-tagging, pdf-ua, wcag, image-alt-text, reading-order, articles-panel, acrobat-accessibility-checker]
level: advanced
status: draft
description: "Export accessible tagged PDFs from InDesign: export tags on styles, Articles reading order, alt text, artifacts, table headers, title and language, checked in Acrobat."
sources:
  - https://helpx.adobe.com/indesign/using/creating-accessible-pdfs.html
  - https://www.pdfa.org/resource/iso-14289-pdfua/
  - https://www.w3.org/WAI/WCAG22/quickref/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessible tagged PDF from InDesign

**Goal:** a PDF that screen readers announce in the right order with headings, alt text and tables intact (PDF/UA, WCAG).

## In InDesign
1. **Styles with export tags:** each paragraph style > Export Tagging > PDF: Tag `H1`, `H2`, `P`, etc. Body styles `P`.
   (Edit All Export Tags dialog in the Paragraph Styles panel menu does it in one place.)
2. **Reading order:** Window > Articles. Drag frames into articles in the order they should be read; tick
   **Use for Reading Order in Tagged PDF**. Without it, order follows layer/creation order (often wrong).
3. **Alt text:** select each meaningful image > Object > Object Export Options > Alt Text (Custom or from metadata).
   Decorative items: Tagged PDF tab > **Artifact** (background shapes, rules, page furniture).
4. **Tables:** convert header rows to real header rows (see header rows skill); avoid tables built from tabs.
5. **Lists:** use InDesign bullets and numbering, not typed characters.
6. **Hyperlinks** via the Hyperlinks panel with meaningful text.
7. **Document title and language:** File > File Info > Title; Character panel language set correctly on styles.
8. Colour contrast and minimum text size per WCAG (see text contrast skill).

## Export (Adobe PDF Print or Interactive)
- Tick **Create Tagged PDF**; **Use Structure for Tab Order** (interactive).
- Advanced > Display Title: **Document Title**; Language set.
- Include Bookmarks and Hyperlinks.

## Check and finish in Acrobat Pro
- **Accessibility > Full Check** (Accessibility Checker): fix flagged items (reading order, figures without alt text, tagged content).
- **Reading Order** tool / Tags panel to inspect.
- For formal **PDF/UA** compliance, validate with **PAC** (PDF Accessibility Checker, free) - Acrobat's check alone is not proof of conformance.

## Gotchas
- Text converted to outlines or placed as images is invisible to screen readers.
- Anchored objects and threaded stories export in story order - anchor sidebars where they belong in the reading flow.
- Every edit in Acrobat is lost when you re-export from InDesign - fix at the source.

## Verify
- [ ] Acrobat Full Check passes; PAC reports no PDF/UA failures (if required).
- [ ] Screen-reader test (NVDA, VoiceOver) of the first pages reads in the intended order.
