---
id: creative-arts.comics-and-sequential-art.comic-scripting.comic-script-templates-and-writing-tools
name: comic-script-templates-and-writing-tools
category: creative-arts
field: comics-and-sequential-art
product: comic-scripting
tags: [comic-scripting, full-script, comic-script-template, scrivener-comic-script, google-docs, word-styles, final-draft, script-export]
level: practitioner
status: draft
description: "Set up a reusable comic script template in Word/Docs styles or Scrivener (page/panel/dialogue styles, auto page breaks) and export clean PDFs for artists and letterers."
sources:
  - https://www.literatureandlatte.com/scrivener/overview
  - https://support.google.com/docs/answer/116338
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Writing+Comics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Comic script templates and writing tools

**Goal:** a template that enforces consistent page/panel/dialogue formatting so you
write story, not formatting, and exports a clean PDF and text copy.

## Option A: Word / Google Docs paragraph styles (most portable)
Create named styles and use them only:
| Style | Settings |
|---|---|
| `Page` | bold caps, 14 pt, "page break before" ON |
| `Panel` | bold, 12 pt, space before 12 pt |
| `Description` | regular 12 pt, left aligned |
| `Dialogue` | 12 pt, hanging indent ~1.5 in so text aligns after `NAME:`; tab stop at the indent |
| `Note` | italic, grey, for editor/artist notes |

- In Docs: Format > Paragraph styles > Update "Heading 1" to match = `Page`, Heading 2 =
  `Panel`. Headings then appear in the document outline, giving a clickable page list.
- In Word: use the Navigation Pane with Heading styles for the same effect.
- Numbering: type numbers by hand or use Word multi-level list numbering for pages
  restarting panel numbers. Auto-numbering breaks on copy/paste into other tools; most
  writers type numbers and re-check (see
  `creative-arts.comics-and-sequential-art.comic-scripting.page-and-panel-numbering-in-full-scripts`).

## Option B: Scrivener
- One document per page inside a folder per issue; the binder becomes a page list you
  can drag to reorder.
- Project > Project Settings > Section Types: `Page`, `Panel`. Compile format applies
  the page header ("PAGE <$n:page>") and page breaks automatically on export.
- Compile to .docx or PDF for collaborators; never send the .scriv bundle.

## Option C: screenwriting apps
Final Draft and similar have comic-book templates, but output conventions vary; check
the artist can read it and that balloon numbers survive.

## Export checklist
- PDF for the artist (fixed layout, page per comic page if possible).
- .docx or plain text for the letterer (they paste dialogue; PDF copy-paste mangles
  line breaks and smart quotes).
- File naming: `title_issue##_script_v#_YYYY-MM-DD`.

## Gotchas
- Smart quotes and em dashes paste as odd glyphs in some lettering fonts; ask the
  letterer which they want.
- Track changes left on in a delivered .docx confuses collaborators; accept/reject first.
- Docs "page break before" on the `Page` style is what keeps one comic page per sheet.

## Verify
- [ ] All text uses template styles (no manual bold for headers).
- [ ] Outline/binder shows every page in order.
- [ ] PDF and editable copies exported; versions dated.
