---
id: computing-software.general-digital-literacy.office-suites.mail-merge-labels
name: mail-merge-labels
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, mail-merge, envelopes-and-labels, mail-merge-labels, address-labels, avery]
level: practitioner
status: docs-checked
description: "Print address labels from an Excel list with Word mail merge, picking the label product, updating all labels and fixing ZIP and date formatting."
sources:
  - https://support.microsoft.com/en-us/word/training/print-labels-for-your-mailing-list
  - https://support.microsoft.com/en-us/excel/create-and-print-mailing-labels-for-an-address-list-in-excel
  - https://support.microsoft.com/en-us/word/use-mail-merge-in-word-to-send-bulk-email-messages
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Mail merge labels from a list

## Prepare the list (Excel)
- Column names that match the fields you want on the labels (FirstName, LastName, Address1, City,
  Postcode), one person per row, all data on the **first sheet**, file stored on your computer.
- Format postcode/ZIP columns as **Text** so leading zeros (02134) survive.
- Finish changes to the list before connecting it to the Word document.

## Merge (Word for Windows)
1. New blank document › **Mailings › Start Mail Merge › Labels** › Label Options: choose the label
   supplier in *Label vendors*/*Label products* and the **Product number** printed on the label pack ›
   OK. No match? **New Label**, enter the dimensions and name it.
2. If no label outlines show, Table Layout › **View Gridlines**.
3. **Select Recipients** › use the existing Excel list; edit, sort or filter recipients as needed.
4. In the first label: **Address Block** or **Insert Merge Field** for each field, with spaces and
   line breaks between, and format it.
5. **Update Labels** copies the first label's layout to all the others.
6. **Preview Results**, then **Finish & Merge › Edit Individual Documents** (check) or **Print Documents**.
- Alternative: Mailings › Start Mail Merge › **Step-by-Step Mail Merge Wizard** › Labels walks through
  the same steps ("Update all labels").

## Gotchas
- Only the first label filled after preview = you skipped *Update Labels*.
- Leading zeros lost or dates shown oddly: fix the number formats in Excel before merging.
- Print a test on plain paper and hold it against the label sheet before using labels.

## Verify
- [ ] Preview the last record: it lands on the correct label and nothing spills to a second line.

## Checked
2026-10-27 against Microsoft Support (Print labels for your mailing list; Create and print mailing labels
for an address list in Excel; email merge page for ZIP formatting), Word for Microsoft 365/2024/2021.
Confirmed: Excel preparation checklist, Label Options vendor/product/New Label, View Gridlines, Select
Recipients, Address Block/Insert Merge Field, Update Labels, Preview Results, Finish & Merge options and
the wizard route. Removed unconfirmed product numbers, field-switch syntax, partial-sheet and Mac notes.
Method: documentation only; no commands were run.
