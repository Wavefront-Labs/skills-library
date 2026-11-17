---
id: computing-software.general-digital-literacy.office-suites.double-sided-and-page-range-printing
name: double-sided-and-page-range-printing
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, double-sided-printing, print-page-range, duplex, manual-duplex, flip-on-long-edge, print-selection]
level: intro
status: docs-checked
description: "Print on both sides (automatic or manual duplex, or odd then even pages) and print only certain pages or a selection in Word and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/print-on-both-sides-of-the-paper-duplex-printing-in-word
  - https://support.microsoft.com/en-us/word/print-a-document-in-word
  - https://help.libreoffice.org/latest/en-US/text/shared/01/01130000.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Double-sided and page-range printing

**Goal:** save paper and print only what's needed.

## Two-sided in Word
- **Check support:** File › Print › under *Settings* open **Print One Sided**. If **Print on Both Sides**
  is listed, the printer can duplex automatically.
- **No duplex unit:** choose **Manually Print on Both Sides**; Word prompts you to turn the stack over and
  feed it in again. Run a test first to learn which way your printer needs the stack reloaded.
- **Odd then even:** *Print All Pages* › **Only Print Odd Pages**, print, flip the stack, then **Only
  Print Even Pages**. If pages come out in the wrong order, File › Options › Advanced › *Print* section:
  *Print on front of the sheet for duplex printing* or *Print on back of the sheet for duplex printing*.

## Two-sided in LibreOffice
File › Print: print *Odd pages*, reinsert the stack, then *Even pages*; tick *Print in reverse order* if
your printer needs it.

## Page ranges
- Word: *Print Current Page*, or **Custom Print** with `1-3` or `3, 4-6` in the Pages box.
- LibreOffice: *Pages* with a list, or **Selection** to print only the selected text or objects.

## Gotchas
- An odd page count on duplex leaves a blank back on the last sheet.

## Verify
- [ ] Back of page 1 is page 2 and upright.

## Checked
- 2026-10-27, against Microsoft Support (Word for Microsoft 365) and LibreOffice help (master) as
  published on that date: how to check for duplex support, Manually Print on Both Sides, Only Print
  Odd/Even Pages and the front/back duplex options, Print Current Page and Custom Print syntax;
  LibreOffice odd/even pages, reverse order, Pages and Selection ranges.

Method: documentation only; no commands were run.
