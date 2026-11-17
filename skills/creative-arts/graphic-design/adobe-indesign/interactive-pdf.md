---
id: creative-arts.graphic-design.adobe-indesign.interactive-pdf
name: interactive-pdf
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, preflight, indesign-export, interactive-pdf, pdf-forms, form-fields, hyperlinks, bookmarks, buttons, page-transitions, fillable-pdf]
level: practitioner
status: draft
description: "Export interactive PDFs from InDesign: hyperlinks and bookmarks, buttons and navigation, fillable form fields with tab order, view settings and file-size control."
sources:
  - https://helpx.adobe.com/indesign/using/dynamic-pdf-documents.html
  - https://helpx.adobe.com/indesign/using/creating-pdf-forms.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interactive PDF

**Goal:** a screen PDF (reports, portfolios, forms) with working links, navigation and fillable fields.

## Links and bookmarks
- **Hyperlinks panel:** select text or frame > New Hyperlink: URL, Email, Page, Text Anchor, Shared Destination.
  Apply a character style (e.g. `Link`) for visible link text. URLs typed in text: Hyperlinks panel menu > Convert URLs to Hyperlinks.
- **Bookmarks panel:** add manually, or generate from the TOC (Create PDF Bookmarks in TOC options).
- **Cross-references** become links automatically.

## Buttons and navigation
Window > Interactive > Buttons and Forms: convert an object to a button; event (On Release or Tap) > action
(Go To Next/Previous Page, Go To Destination, Go To URL, Show/Hide Buttons and Forms). Put navigation buttons on parent pages.

## Forms (fillable fields)
- Buttons and Forms panel > Type: **Text Field**, Check Box, Radio Button (same name, different values = group),
  Combo Box, List Box, Signature Field, Button (Print Form, Submit Form, Clear Form).
- Set name, description (tooltip and accessibility), font size (Auto or fixed), Required, Multiline.
- **Tab order:** Object > Interactive > Set Tab Order.
- Complex forms (calculations, validation, scripts) need finishing in Acrobat Pro > Prepare Form.

## Export (File > Export > Adobe PDF (Interactive))
- Pages or **Spreads** (for reading on screen, spreads suit facing-page designs; single pages suit phones).
- **View:** Fit Page; **Layout:** Single Page / Two-Up (Cover Page); Open in Full Screen Mode for kiosks.
- **Forms and Media:** Include All; Page transitions optional.
- **Create Tagged PDF** and Use Structure for Tab Order (accessibility, see accessible PDF skill).
- **Compression:** JPEG 2000 or JPEG, resolution 144-150 ppi for screen; RGB colour (convert to sRGB destination).

## Gotchas
- Print PDF/X presets strip interactivity; export separately.
- Form field fonts: embedded only for the field's typed content in Acrobat if set; use common fonts.
- Hidden objects on master pages still clickable if they are buttons - check navigation in Acrobat.

## Verify
- [ ] Every link and button tested in Acrobat Reader (not just a browser viewer).
- [ ] Form tab order logical; fields fillable and printable; file size suitable for email.
