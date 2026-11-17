---
id: computing-software.general-digital-literacy.office-suites.booklet-printing
name: booklet-printing
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, printing-documents, booklet-printing, book-fold, pages-per-sheet, duplex]
level: practitioner
status: docs-checked
description: "Print an A5 booklet from an A4 Word document with Book fold, or several pages per sheet, getting page order and double-sided flipping right."
sources:
  - https://support.microsoft.com/en-us/word/create-a-booklet-or-book-in-word
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Booklet printing

**Goal:** a folded, stapled booklet where pages come out in reading order.

## Word: Book fold
1. **Layout > Margins > Custom Margins**, then **Multiple pages > Book fold**. The orientation changes to landscape automatically.
2. Under **Sheets per booklet** choose how many pages print per booklet; split a long document into several booklets if needed.
3. Increase the **Gutter** to leave room on the inside fold for binding.
4. On the **Paper** tab choose the paper size: the finished booklet is half the paper's width (A4 sheets give A5 pages).
5. **File > Print**: if the printer supports automatic two-sided printing, choose **Booklet** under **Two-sided**. Otherwise print manually on both sides and flip the sheets on the short edge as your printer's instructions say.
6. Fold the stack in half and staple on the fold.

## Gotchas
- Check the paper size under File > Page Setup / the Paper tab against what is in the tray.
- Add page numbers in the header or footer for a polished result.
- Print one test sheet first and fold it.

## Verify
- [ ] Print the first two sheets, fold: pages read 1, 2, 3, 4... with nothing upside down.

## Checked

2026-10-27. Microsoft Support 'Create a booklet or book in Word' (Windows and Mac listed, read 2026-10-27): Book fold path, Sheets per booklet, Gutter, half-width paper size, Booklet under Two-sided, manual duplex flip on the short edge. Removed: multiple-of-4 rule, Acrobat Reader booklet steps, pages-per-sheet steps, odd/even header advice and the long-edge upside-down claim (not documented).

Method: documentation only; no commands were run.
