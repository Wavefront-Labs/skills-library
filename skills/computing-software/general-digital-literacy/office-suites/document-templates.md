---
id: computing-software.general-digital-literacy.office-suites.document-templates
name: document-templates
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, document-templates, templates, dotx, ott, template-gallery, google-docs-templates, letterhead]
level: intro
status: docs-checked
description: "Start documents from built-in or custom templates in Word, Google Docs and LibreOffice, and save your own letterhead or report layout as a reusable template."
sources:
  - https://support.microsoft.com/en-us/word/save-a-word-document-as-a-template
  - https://support.microsoft.com/en-us/word/create-a-template
  - https://support.google.com/docs/answer/148833
  - https://help.libreoffice.org/latest/en-US/text/shared/01/01110300.html
  - https://help.libreoffice.org/latest/en-US/text/shared/04/01010000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working from document templates

**Goal:** stop rebuilding the same letter, invoice or report layout; start from a template.

## Use a ready-made template
- **Word:** File › New › pick a template category and a template.
- **Google Docs:** on the Docs home screen click **Template Gallery** (top right); a copy of the
  template opens. Inside a document, File › New › From a template inserts one.
- **LibreOffice:** File › Templates (`Ctrl+Shift+N`) opens the Template Manager.

## Make your own
- **Word:** build the document (styles, logo in the header, placeholder text such as
  `[Client name]`) › File › Save As › type **Word Template (.dotx)** (`.dotm` only if it has
  macros). Word saves it in the *Custom Office Templates* folder under Documents; start a new
  document from it with File › New › **Personal** (may say *Custom*).
- **Google Docs (personal accounts):** keep a master doc named `TEMPLATE - Invoice` and use
  File › Make a copy each time.
- **LibreOffice:** File › Templates › **Save as Template** › name it and pick a category; it then
  appears in the Template Manager.

## Gotchas
- To edit a Word template itself, open it with File › Open from the Custom Office Templates folder,
  change it and save.
- Editing a copy never changes the template, and changing the template never updates documents
  already made from it.
- Put repeating elements in styles and headers, not typed formatting, so the template stays
  consistent.

## Verify
- [ ] A new document from your template opens as a new untitled document, not as the template file.
- [ ] Logo, styles and margins are already in place.

## Checked
2026-10-27 against Microsoft Support Word template pages (Microsoft 365), Google Docs Editors Help (Use
templates) and the LibreOffice help (master). Confirmed: .dotx/.dotm and the Custom Office Templates
folder and File › New › Personal; Docs Template Gallery, File › New › From a template and File › Make
a copy; LibreOffice File › Templates › Save as Template and Ctrl+Shift+N. Removed unconfirmed claims
about double-click behaviour, the .ott extension and Workspace gallery submission. Method: documentation only; no commands were run.
