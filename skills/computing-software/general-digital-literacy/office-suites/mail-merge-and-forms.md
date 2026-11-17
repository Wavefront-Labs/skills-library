---
id: computing-software.general-digital-literacy.office-suites.mail-merge-and-forms
name: mail-merge-and-forms
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, mail-merge, word-mail-merge, google-forms, microsoft-forms, labels, personalised-letters, bulk-email, data-source, merge-fields, form-responses]
level: intro
status: docs-checked
description: "Generate personalised letters, labels or emails from a spreadsheet with mail merge in Word/Google Docs, and build a simple data-collecting form."
sources:
  - https://support.google.com/docs/answer/6281888
  - https://support.google.com/docs/answer/2917686
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mail merge and forms — one template, many people, and a form that collects it back

**Goal:** turn a spreadsheet of names/addresses into personalised letters, labels, or
emails without typing each one by hand, and set up a simple form to collect structured
responses from other people.

## 1. The mail merge concept
Mail merge combines a **template** (the letter/label/email, with placeholders) and a
**data source** (a spreadsheet, one row per recipient) to produce one output per row.
Get the spreadsheet clean first, because merge problems are almost always data problems,
not template problems.

## 2. Preparing the data source
- One **header row** naming each field (`FirstName`, `Address1`, `City`...), one row per
  recipient, no merged cells or blank rows.
- Keep postcodes and phone numbers as **Text** so leading zeros are not lost.
- Remove rows for anyone who shouldn't receive this merge before running it: a merge
  processes every row present.
- Test with a few real rows (or your own address) and preview before printing or
  sending in bulk.

## 3. Where to find the merge tool
Word, LibreOffice Writer and add-ons for Google Docs/Sheets each provide mail merge with
the same template-plus-data model. The menu names differ by product and version, so
follow the help for the product you use. For labels, choose the label product number
printed on the label packaging so the layout matches the sheet.

## 4. Building a simple form (Google Forms)
- Go to forms.google.com and click Blank form, then name it. A form can also be made
  from Google Drive (New › Google Forms) or from a spreadsheet at sheets.google.com.
- Responses can be stored in a Google Sheet: in the form's Responses tab, open More ›
  Select destination for responses, then create or select a spreadsheet. That Sheet
  can then serve as a mail-merge data source.
- Briefly state on the form what the data will be used for, and do not collect sensitive
  data such as card numbers through a plain form.

## Verify
- [ ] The data source has one clean header row and postcodes/phone numbers kept as text.
- [ ] A merge preview was checked on a few real rows before finishing/sending/printing.
- [ ] A built form has a stated purpose, and responses land somewhere you checked.

## Checked
2026-11-01. Confirmed from Google Docs Editors Help: creating a form (forms.google.com,
Blank form, from Drive or Sheets) and sending responses to a linked Sheet (Select
destination for responses). Removed: Word Mailings-tab steps (Microsoft's mail merge
page returned 404), Outlook merge-to-email, Google Workspace add-on and Marketplace
claims, Microsoft Forms export path, and Excel/CSV formatting claims.
Method: documentation only; no commands were run.
