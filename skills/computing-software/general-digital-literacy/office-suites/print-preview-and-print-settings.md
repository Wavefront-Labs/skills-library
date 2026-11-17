---
id: computing-software.general-digital-literacy.office-suites.print-preview-and-print-settings
name: print-preview-and-print-settings
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, print-preview, printing-documents, printer-properties, scaling, pages-per-sheet, print-settings]
level: intro
status: docs-checked
description: "Use print preview and the print dialog in Word and LibreOffice: choose printer, pages, sides, markup and copies before wasting paper."
sources:
  - https://support.microsoft.com/en-us/word/print-a-document-in-word
  - https://support.microsoft.com/en-us/word/print-on-both-sides-of-the-paper-duplex-printing-in-word
  - https://help.libreoffice.org/latest/en-US/text/shared/01/01130000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Print preview and print settings

**Goal:** print exactly what you meant, once.

## Word
**File › Print** shows the preview beside the settings. Under **Settings**, the first drop-down (*Print
All Pages* by default) holds the page options:
| Need | Setting |
|---|---|
| Only the page on screen | **Print Current Page** |
| A range or a mix | **Custom Print** › Pages box, e.g. `1-3` or `3, 4-6` |
| Comments and tracked changes | **Print Markup** (untick to leave them out) |
| Both sides | *Print One Sided* › **Print on Both Sides** (if the printer supports it) or **Manually Print on Both Sides** |
To print with no comments at all, set **Review › Display for Review › No Markup** first.

## LibreOffice
**File › Print** opens a dialog with a preview, the printer and its **Properties**, and **Range and
copies**: *All pages*, *Pages* (a list you type), *Selection*, plus *Even pages* / *Odd pages* and *Print
in reverse order*. Options vary by printer and operating system.

## Gotchas
- Check the chosen printer: a PDF printer selected by accident "prints" to a file.
- A last page with one line on it? Trim spacing or margins before printing.

## Verify
- [ ] Preview page count and layout match expectations before clicking Print.

## Checked
- 2026-10-27, against Microsoft Support (Word for Microsoft 365) and LibreOffice help (master) as
  published on that date: Word Settings page options (Print Current Page, Custom Print syntax), Print
  Markup and No Markup, one/both-sided and manual duplex options; LibreOffice Print dialog preview,
  printer properties, range options, even/odd pages and reverse order.

Method: documentation only; no commands were run.
