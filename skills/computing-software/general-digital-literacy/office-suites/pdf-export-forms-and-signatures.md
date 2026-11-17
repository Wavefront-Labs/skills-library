---
id: computing-software.general-digital-literacy.office-suites.pdf-export-forms-and-signatures
name: pdf-export-forms-and-signatures
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, pdf, pdf-export, fillable-pdf, pdf-form, e-signature, digital-signature, docusign, adobe-acrobat, preview-sign, flatten-pdf, print-to-pdf]
level: intro
status: draft
description: "Export a clean PDF from any office app, fill or build a basic fillable form, and add a signature that will actually be accepted."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PDF export, forms and signatures — the last step before a document leaves your hands

**Goal:** produce a PDF that looks the same on every device, fill in or build a simple
fillable form, and sign a document in a way that's actually accepted, without buying
software for a one-off task.

## 1. Exporting a clean PDF
- Word/Excel/PowerPoint: File › **Save As** / **Export** › choose PDF (or
  File › Print › Microsoft Print to PDF as a universal fallback that works from any
  Windows app, not just Office).
- Google Docs/Sheets/Slides: File › **Download** › PDF Document.
- macOS: any app's Print dialog › PDF dropdown (bottom-left) › Save as PDF — works from
  literally anything that can print, the macOS equivalent of Print to PDF.
- Exporting to PDF **freezes the layout** — fonts, page breaks and formatting stay fixed
  regardless of what app or OS opens it next, which plain `.docx`/`.pptx` cannot
  guarantee across different apps/versions (see office-suite-essentials, section 4).
- Check the PDF **before sending**: page breaks landed where expected, no cut-off text
  at page edges, and (for a scanned/image-based source) that the text is actually
  readable, not blurry from over-compression.

## 2. Filling an existing PDF form
- Adobe Acrobat Reader (free) and Preview (macOS, built in) both detect **fillable
  fields** automatically when opening a form PDF — click into a field and type; a
  highlighted/bordered box on hover usually signals a genuine fillable field.
- A PDF with **no detected fields** ("flat" scan of a paper form) still gets filled in
  Acrobat Reader via **Fill & Sign** mode, which lets you click anywhere to drop a text
  box — it's not a true form field, just text placed on top of the image, but it works
  for a one-off submission.
- Save a filled form as a **new file name** before submitting, so you keep a record of
  exactly what was submitted.

## 3. Building a simple fillable form
- In Acrobat (the full paid version, or the free online tools some vendors offer): Open
  › **Prepare Form** — it auto-detects likely fields from a Word-exported PDF's layout
  (underlines, boxes) and lets you add text fields, checkboxes and signature fields
  manually where it guesses wrong.
- A lighter free alternative for most everyday needs: build the form as a **Google
  Form** instead (see mail-merge-and-forms, section 6) if a fillable PDF specifically
  isn't required by whoever's receiving it — far less setup for the same outcome when a
  PDF format isn't a hard requirement.
- **Flatten** the finished form (Acrobat: Print to a new PDF, or Prepare Form ›
  flattening option) before distributing if you want the layout locked and uneditable
  once someone later fills it — otherwise a recipient could alter the form's structure,
  not just the answers.

## 4. E-signatures
- **Typed/drawn signature in Preview (Mac) or Acrobat Reader (Fill & Sign › Sign)**:
  good enough for most everyday, low-stakes documents (an internal form, a simple
  agreement between people who know each other) — draw with trackpad/mouse, or use the
  trackpad-signature-via-camera option in Preview, or type your name in a script font.
- **Dedicated e-signature services** (DocuSign, Adobe Sign, HelloSign and similar): add
  an audit trail (timestamp, IP address, identity verification steps) that a typed
  signature in Preview doesn't — use these for anything that might need to be defended
  as legally binding (contracts, official forms), not a simple typed/drawn signature.
- **Legal validity varies by country and document type** — most jurisdictions recognise
  electronic signatures broadly (e.g. under ESIGN/UETA in the US, eIDAS in the EU), but
  some document categories (wills, certain property transfers) specifically still
  require a wet-ink or notarised signature. If in doubt for anything high-stakes, check
  with whoever is requiring the signature before assuming any e-signature method will
  be accepted — this is a legal question beyond this skill's scope, say so explicitly.

## Verify
- [ ] An exported PDF was opened and checked (page breaks, readability) before sending.
- [ ] A filled PDF form was saved under a new filename before submitting, as a record.
- [ ] A form you distribute was flattened if the layout should stay locked.
- [ ] You matched the signature method's rigor to the stakes of the document, and asked
      the requester directly if a dedicated e-signature service might be required.
