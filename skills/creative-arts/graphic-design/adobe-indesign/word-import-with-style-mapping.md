---
id: creative-arts.graphic-design.adobe-indesign.word-import-with-style-mapping
name: word-import-with-style-mapping
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-text-frames, text-threading, word-import-style-mapping, microsoft-word-import-options, style-import, remove-local-formatting, manuscript-cleanup]
level: practitioner
status: draft
description: "Import Word manuscripts into InDesign cleanly: Import Options, mapping Word styles to InDesign styles, dropping local formatting while keeping italics, and saved presets."
sources:
  - https://helpx.adobe.com/indesign/using/importing-files-applications.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Importing Word with style mapping

**Goal:** a manuscript placed with every paragraph in the right InDesign style and none of Word's stray formatting.

## Ask the author for clean Word files
Headings with Word's Heading 1/2/3 styles, body in Normal, no manual spacing with empty paragraphs or
tabs, italics as real italics (or an Emphasis character style). Clean source = clean import.

## Place with Show Import Options
File > Place, tick **Show Import Options**, select the .docx:
- **Include:** Table of Contents Text (usually off), Index Text, Footnotes, Endnotes.
- **Use Typographer's Quotes** on.
- **Formatting:**
  - **Remove Styles and Formatting from Text and Tables** with **Preserve Local Overrides** ticked
    keeps italics/bold but drops fonts - quick and fairly safe.
  - Better: **Preserve Styles and Formatting** + **Customize Style Import** > **Style Mapping...**: map
    Word `Heading 1` -> InDesign `H1`, `Normal` -> `Body`, `Quote` -> `Extract` etc.
    Conflict option: **Use InDesign Style Definition** (Word's version of the style is ignored).
  - **Manual Page Breaks:** No Breaks (let your layout decide).
  - Import Inline Graphics: usually off (place images separately at proper resolution).
- **Save Preset** for the series.

## After import
- Paragraph Styles panel: Word-only styles appear with a disk icon - map or delete (replace with your style).
- Remove local overrides that slipped through: select body text, Alt/Option+click the style (or Clear Overrides),
  but protect italics first with a character style (Find/Change: Font Style Italic -> character style `Italic`).
- Clean double spaces, double returns, tabs-as-indents with Find/Change (see find/change skill).
- Keep the Word file **linked** only if edits will come back in Word (Preferences > File Handling > Create Links
  When Placing Text); otherwise unlink to avoid accidental overwriting.

## Gotchas
- Word's "Normal" with different fonts per paragraph (local formatting) imports as overrides - Clear them.
- Tracked changes and comments: accept/remove in Word first; InDesign can import them as Track Changes but it rarely helps.
- Endnotes import as InDesign endnotes (2018+); check numbering style afterwards (see footnotes skill).

## Verify
- [ ] No Word-origin styles left in the panel; no + overrides in body text.
- [ ] Italics and bold preserved via character styles.
- [ ] Import preset saved for future chapters.
