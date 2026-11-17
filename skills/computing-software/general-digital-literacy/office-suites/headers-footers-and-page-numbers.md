---
id: computing-software.general-digital-literacy.office-suites.headers-footers-and-page-numbers
name: headers-footers-and-page-numbers
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, headers-and-footers, page-numbers, different-first-page, page-x-of-y, google-docs-header, link-to-previous]
level: intro
status: docs-checked
description: "Add headers, footers and page numbers, use a different first page, Page X of Y and restart numbering per section in Word, Google Docs and LibreOffice."
sources:
  - https://support.microsoft.com/en-us/word/start-page-numbering-later-in-your-document
  - https://support.microsoft.com/en-us/word/customize-page-numbers-and-their-formats-in-different-word-document-sections
  - https://support.microsoft.com/en-us/word/link-to-previous
  - https://support.google.com/docs/answer/86629
  - https://support.google.com/docs/answer/179738
  - https://help.libreoffice.org/latest/en-US/text/swriter/guide/header_footer.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/guide/pagenumbers.html
  - https://help.libreoffice.org/latest/en-US/text/swriter/00/00000404.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Headers, footers and page numbers

**Goal:** every page carries the right title, date or number automatically.

## Add them
- **Word:** Insert › Header or Footer › Edit Header/Edit Footer; Insert › Page Number (choose
  position). Leave with **Close Header and Footer**, `Esc`, or a double-click outside the header.
- **Google Docs:** Insert › Page elements › Header / Footer / Page number (Page number, Page count or
  More options). Keyboard: hold `Ctrl+Alt`, press `O` then `H` for the header. Only in *pages* format,
  not pageless.
- **LibreOffice Writer:** Insert › Header and Footer › Header › pick the page style; Insert › Page
  Numbers opens a guided dialog, or Insert › Field › Page Number at the cursor.

## Common needs
- **No number on the cover page:** Word: Header & Footer › **Different First Page**; Docs: click the
  header and tick *Different first page*; LibreOffice: give the cover the *First Page* page style
  (View › Styles › Page Styles › double-click "First Page").
- **Page X of Y:** LibreOffice: Insert › Field › Page Count after the page number. Google Docs:
  Insert › Page elements › Page number › Page count inserts the total.
- **Start numbering at 1 after the contents pages (Word):** Layout › Breaks › **Next Page**, then in
  the new section's header/footer deselect **Link to Previous** and use Page Number › Format Page
  Numbers › *Start at* 1. Docs: Page number › More options › Apply to a section.
- **Odd/even** (books): Word *Different Odd & Even Pages*; Docs: Options › Apply to Whole document ›
  Different odd and even.

## Gotchas
- Typing "Page 3" by hand never updates; always insert the page-number field.
- With Link to Previous on, a section's header carries over from the previous section; headers and
  footers are linked separately.
- If Link to Previous is dimmed, there is no section break yet.

## Verify
- [ ] Page numbers in print preview run in sequence, cover page blank if wanted.

## Checked
2026-10-27 against Microsoft Support Word page-numbering pages (Microsoft 365, 2024, 2021), Google Docs
Editors Help (headers, footers, page numbers; shortcuts) and the LibreOffice help (master). Confirmed:
the Word, Docs and LibreOffice insert paths, Different First Page, Next Page break plus Link to Previous
and Start at, odd/even options, LibreOffice First Page style and Page Count field, Docs page count.
Corrected Google Docs menus to Insert › Page elements. Removed an unconfirmed Word Page X of Y gallery
path and header-distance tip. Method: documentation only; no commands were run.
