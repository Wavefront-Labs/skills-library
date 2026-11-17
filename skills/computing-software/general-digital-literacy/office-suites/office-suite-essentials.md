---
id: computing-software.general-digital-literacy.office-suites.office-suite-essentials
name: office-suite-essentials
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, microsoft-365, word, excel, powerpoint, google-workspace, google-docs, google-sheets, google-slides, libreoffice, writer, calc, impress, styles, headings, table-of-contents, track-changes, suggesting-mode, version-history, cell-references, freeze-panes, csv, pdf-export, keyboard-shortcuts, word-processing, spreadsheets, presentations]
level: intro
status: draft
description: "Core habits for Word/Docs/Writer, Excel/Sheets/Calc and PowerPoint/Slides: styles not manual formatting, sane spreadsheets, master slides, review and sharing."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Office suite essentials — documents, spreadsheets, slides that don't fight you

**Goal:** produce documents, spreadsheets and decks that stay tidy when edited, shared
or converted, in any of Microsoft 365, Google Workspace or LibreOffice. The habits below
are the same in all three; only the menus differ. Shortcuts are Windows/Linux — on a Mac
use Cmd for Ctrl unless noted.

## 1. Documents: structure with styles, never with spaces
- Mark headings with **Heading 1 / Heading 2 styles**, not bold + bigger font. Shortcuts:
  Word and Google Docs `Ctrl+Alt+1`/`2`/`3`; LibreOffice Writer `Ctrl+1`/`2`/`3`;
  normal text is `Ctrl+Alt+0` (Docs) or `Ctrl+0` (Writer). In Word use the Styles gallery.
- Headings give you a free outline (Word: View › Navigation Pane; Docs: the outline
  icon at the left; Writer: Navigator, `F5`) and an automatic **table of contents**
  (Word: References › Table of Contents; Docs: Insert › Table of contents; Writer:
  Insert › Table of Contents and Index). Update it after editing — it does not refresh itself
  in Word or Writer.
- To change the look of every heading, **modify the style** once rather than
  reformatting each one.
- Start a new page with `Ctrl+Enter` (page break), never by pressing Enter repeatedly.
  Turn on formatting marks (Word `Ctrl+Shift+8`; Writer `Ctrl+F10`) to see stray
  spaces, tabs and breaks.
- Paste text from the web/email **without formatting**: Google Docs `Ctrl+Shift+V`;
  LibreOffice `Ctrl+Alt+Shift+V`; Word: Paste Options › Keep Text Only (recent
  Microsoft 365 builds also accept `Ctrl+Shift+V` — unconfirmed for every channel).

## 2. Spreadsheets: one table, one fact per cell
- One header row, one record per row, no blank rows or merged cells inside the data.
  Merged cells break sorting, filtering and pivot tables.
- **Freeze the header** (Excel/Calc: View › Freeze Panes › Freeze Top Row / Freeze First
  Row; Sheets: View › Freeze › 1 row). Turn the range into a table with `Ctrl+T` in Excel
  to get filters and auto-extending formulas.
- References: `A1` moves when copied, `$A$1` does not. Press `F4` while editing a
  reference to cycle through the `$` options (Excel and Sheets; Calc uses `Shift+F4`).
- Jump to the data edge with `Ctrl+Arrow`; select to it with `Ctrl+Shift+Arrow`.
- Core functions worth knowing: `SUM`, `AVERAGE`, `COUNTIF`, `SUMIF`, `IF`, and a lookup
  (`XLOOKUP` in Excel 2021/365 and Google Sheets; `VLOOKUP` everywhere, with the
  last argument `FALSE` for an exact match — forgetting it is the classic bug).
- **Gotcha — auto-conversion.** Opening a CSV silently turns `00123` into `123`, long
  IDs into `1.23E+15`, and codes like `MARCH1` or `1-2` into dates. Import via
  Data › From Text/CSV (Excel) or File › Import (Sheets) and set those columns to Text,
  or prefix a single value with an apostrophe (`'00123`).
- Dates are numbers formatted as dates; if a "date" left-aligns, it is text and will
  not sort or calculate correctly.

## 3. Presentations: design once on the master
- Put logos, fonts and colours on the **slide master** (PowerPoint: View › Slide Master;
  Slides: Slide › Edit theme; Impress: View › Master Slide), then use the built-in
  layouts so titles land in title placeholders — that also makes the outline and
  accessibility readers work.
- One idea per slide, large type (aim for 24 pt+ body text in a room), speaker notes for
  the rest. Rehearse with **Presenter View** so the audience sees slides and you see notes.
- Add alt text to images (right-click › alt text in all three suites).

## 4. Reviewing, versions and sharing
- Ask for edits as **Track Changes** (Word: Review › Track Changes, `Ctrl+Shift+E`;
  Writer: Edit › Track Changes › Record, `Ctrl+Shift+C`) or **Suggesting** mode in
  Google Docs (mode menu at top right). Accept/reject before you finalise.
- Recover old versions: Google files File › Version history; Microsoft 365 files saved to
  OneDrive/SharePoint File › Info › Version History. Local files without AutoSave only
  have what you saved — save early, with `Ctrl+S`.
- Share **a link with the right permission** (Viewer / Commenter / Editor) instead of
  emailing copies; one live file avoids "which version is current?". Check whether the
  link is restricted to named people or "anyone with the link".
- For anything final or going to an unknown recipient, **export to PDF**
  (File › Save As / Download / Export as PDF). Cross-suite opening (`.docx` in
  LibreOffice, `.pptx` in Slides) can shift fonts and layout; PDF freezes it.

## Verify
- [ ] Every heading uses a Heading style; the navigation pane/outline shows the structure.
- [ ] The table of contents is updated and page breaks are real breaks.
- [ ] Spreadsheet data is one table with a frozen header, no merged cells, IDs with leading zeros intact.
- [ ] Copied formulas give correct results down the column (absolute refs where needed).
- [ ] Slides use master layouts; images have alt text.
- [ ] Shared link permissions are what you intend; finals sent as PDF.
