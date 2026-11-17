---
id: languages-linguistics.braille-and-tactile-literacy.duxbury.importing-translating-and-embossing-in-duxbury-dbt
name: importing-translating-and-embossing-in-duxbury-dbt
category: languages-linguistics
field: braille-and-tactile-literacy
product: duxbury
tags: [duxbury, dbt, duxbury-braille-translator, braille-translation-software, braille-translation-tables, ueb, document-templates, styles, dbt-codes, grade-1-code, translation-errors, embosser, embosser-setup, brf, braille-ready-file, word-import, docx, swift, braille-transcription, proofreading]
level: practitioner
status: draft
description: "Produce braille in Duxbury DBT: pick a template and translation table, import Word with styles, fix mistranslations with codes, check pagination and send to an embosser or BRF."
sources: ["Duxbury Systems DBT documentation and knowledge base (paraphrased)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Importing, translating and embossing in Duxbury DBT

**Goal:** go from a print source file to accurate, correctly formatted braille output with
Duxbury Braille Translator, without hand-fixing the same error on every page.

> Uncertainty: menu names and shortcuts below follow recent DBT releases as generally
> documented; they shift between versions. Check *Help* in your installed version.

## 1. Set up the document correctly first
- **Template = code + format.** Start a new document from a template for the target code and
  format convention (e.g. a UEB template matching your national formatting rules). The
  template sets the **translation table**, page size (cells × lines) and style definitions.
- Confirm under the **Document** menu: translation table/language, braille page size and
  page-numbering settings. A wrong table is the root of most "DBT gets it wrong" complaints.
- Set **embosser setup** once (Global/Document embosser settings): model, paper size,
  interpoint (double-sided) or single-sided.

## 2. Import with structure, not just text
- Prepare the Word source: use **real heading styles**, real lists and real tables. DBT maps
  Word styles to braille styles on import; manual bold-and-large "headings" come through as
  plain emphasised text and format wrongly.
- Remove print-only clutter (running headers, decorative images, text boxes) or decide how to
  treat them before import.
- Import with File › Open (choosing the Word file) and check the import options for how
  emphasis, images and page breaks are handled.

## 3. Translate and inspect
- Translate the print document to a braille document (File › Translate, often Ctrl+T in the
  versions we've seen). The braille file is a **separate document** — fix structural issues
  in the print side and re-translate where possible, so fixes survive re-translation.
- Turn on **codes view** to see the style and format codes surrounding text. Most formatting
  surprises are a stray or missing code.
- Use **styles** consistently (headings, lists, poetry, transcriber's notes) rather than
  manual spacing; manual blank lines break page layout after edits.

## 4. Fixing mistranslations
Typical problems: proper names and foreign words contracted wrongly, URLs and emails
contracted, emphasis lost, a contraction bridging a word-part boundary.
- Apply DBT's **grade-1 / uncontracted codes** around a word or passage on the print side
  to force uncontracted output.
- For repeated names in a long book, use the **exceptions/dictionary** mechanism rather than
  coding every instance (feature names vary by version).
- Mark **foreign-language passages** with language codes so the right table is used.
- After every fix type, re-translate and spot-check a later instance.

## 5. Pagination and output
- Review print page numbers, braille page numbers, and that no heading sits alone at the
  bottom of a page.
- Output to the **embosser** (File › Emboss) or save a **BRF** (braille-ready file) for
  readers using displays/notetakers. A BRF has fixed line length — use the reader's cells per line.
- Emboss a **test page** first: check dot quality, margins and interpoint alignment.

## Gotchas
- Translation software is not a transcriber: maths, tables, poetry and complex formats still
  need human judgement and a human proofread (see the braille-transcription skill).
- Editing only the braille side means fixes are lost if anyone re-translates later; record
  braille-side edits or avoid them.
- Embosser driver vs DBT embosser setup conflicts cause blank or doubled pages — set paper
  size and duplexing in one place.

## Verify
- [ ] Template, translation table and page size match the reader's requirements.
- [ ] Headings and lists arrive as DBT styles, not as manual emphasis.
- [ ] Names, URLs and foreign words checked; recurring fixes applied via codes/exceptions.
- [ ] Pagination reviewed; test page embossed or BRF opened on a display.
- [ ] Final braille proofread per the transcription proofreading method.
