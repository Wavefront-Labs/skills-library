---
id: computing-software.general-digital-literacy.office-suites.envelopes-and-labels
name: envelopes-and-labels
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, envelopes-and-labels, address-labels, avery, label-templates, print-envelope, return-address]
level: intro
status: docs-checked
description: "Print a single envelope or a sheet of address labels (Avery and similar) from Word or LibreOffice Writer, testing alignment on plain paper first."
sources:
  - https://support.microsoft.com/en-us/office/create-and-print-a-single-envelope-in-word-b766aa84-5b97-4f63-b03f-451d2fb3640f
  - https://support.microsoft.com/en-us/word/create-a-sheet-of-nametags-or-address-labels-in-word
  - https://support.microsoft.com/en-us/office/avery-wizard-is-retired-4c1c1aba-fefe-4e66-ad14-5f3b910a85dc
  - https://help.libreoffice.org/latest/en-US/text/shared/guide/labels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Envelopes and labels

**Goal:** print an addressed envelope or a sheet of labels that lines up.

## Word
- **Envelope:** Mailings tab, Create group, **Envelopes**. Enter Delivery and Return addresses. **Options > Envelope Options** sets the envelope size (or Custom size); **Printing Options** sets the **Feed method** (position, long or short edge first, face up or down) to match your printer. **Add to Document** keeps the envelope for reuse; otherwise load the envelope as the Feed diagram shows and Print.
- **Labels:** **Mailings > Labels > Options**, choose the label brand under *Label products* and the *Product number*; **New Label** creates a custom size. **New Document** creates a table sized to the label; turn on gridlines with Layout > Align > View Gridlines if you cannot see it, type the labels and print. On Mac, select your printer type in Options first. Word for the web cannot create labels directly: start from a label template.
- **Many different addresses:** use **Mailings > Start Mail Merge** with a spreadsheet of addresses.
- The old Avery Wizard is retired; Avery-compatible layouts are in the Labels dialog.

## LibreOffice Writer
**File > New > Labels**: on the *Labels* tab pick the format and inscription; on the *Options* tab keep *Synchronize contents* ticked, click **New Document**, type the first label and press **Synchronize Labels** to copy it to the rest. **File > New > Business Cards** works the same way.

## Gotchas
- **Test on plain paper first** and hold it over a label sheet against the light.
- Check the printer's tray diagram for envelope orientation.

## Verify
- [ ] Plain-paper test aligns with every label on the sheet, top and bottom rows included.

## Checked

2026-10-27. Microsoft Support single envelope, nametags/address labels and Avery Wizard retirement pages, and LibreOffice help (guide/labels), read 2026-10-27. Removed: Google Docs add-on claim, Avery A4/A5 vendor names, 'Full page of the same label', Details/pitch adjustment, printer scaling advice and LibreOffice Insert > Envelope (none confirmed on current pages); ICDL source dropped.

Method: documentation only; no commands were run.
