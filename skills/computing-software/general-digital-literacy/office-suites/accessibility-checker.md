---
id: computing-software.general-digital-literacy.office-suites.accessibility-checker
name: accessibility-checker
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, accessible-documents, accessibility-checker, check-accessibility, accessibility-ribbon, grackle, pdf-accessibility, tagged-pdf]
level: intro
status: docs-checked
description: "Run the built-in Accessibility Checker in Word, Excel, PowerPoint and Outlook (or LibreOffice Writer) and fix the common errors before sharing."
sources:
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/improve-accessibility-with-the-accessibility-checker
  - https://support.microsoft.com/en-us/accessibility/office-accessibility/rules-for-the-accessibility-checker
  - https://help.libreoffice.org/latest/en-US/text/swriter/01/accessibility_check.html
  - https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_universal_accessibility.html
  - https://www.w3.org/WAI/fundamentals/accessibility-intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Running the accessibility checker

**Goal:** catch the issues that block screen-reader and low-vision users before you send.

## Microsoft 365
- **Windows or Mac, Word/Excel/PowerPoint:** **Review > Check Accessibility** (the lower half of the button has more options; older Windows versions: File > Info > Check for Issues > Check Accessibility). The web apps (except Outlook on the web) use the same Review tab path.
- **Outlook:** on Windows the Review tab only appears while you write or reply to a message, then Check Accessibility. Outlook for Mac: Edit on the toolbar > Check Accessibility. Outlook on the web: Options on the toolbar > Check accessibility.
- Results are grouped as **Errors**, **Warnings** and **Tips**. Per the rules page: missing alt text, no table header row and missing slide titles are Errors; low text contrast, slide reading order and complex table structure (split cells, merged cells, nesting) are Warnings; unique slide titles and heading styles are Tips.
- Word, Excel and PowerPoint also offer an option to keep the checker running while you work.

## Google Docs / Slides
Check by hand: alt text via the Alt text command (Ctrl+Alt+Y), headings, and text contrast.

## LibreOffice Writer
**Tools > Check Accessibility** reviews the document (title, language, alt text, table structure, fake numbering, link text, contrast, heading order). In the PDF export dialog choose **Universal Accessibility (PDF/UA)**; Tagged PDF is then forced on.

## Gotchas
- The checker cannot judge whether alt text is good or whether colour alone carries meaning; review those by hand.
- Fixing issues in the source document is easier than fixing an exported PDF.

## Verify
- [ ] Checker shows no errors; you have read the warnings and fixed or consciously accepted each one.

## Checked

2026-10-27. Microsoft Support accessibility-checker and rules pages (Word/Excel/PowerPoint/Outlook, Windows, Mac, web, read 2026-10-27); LibreOffice help master (Writer accessibility check, PDF/UA export). Confirmed menu paths, error/warning/tip classes, LibreOffice checks and PDF/UA option. Removed: status-bar wording, PDF structure-tag option, Grackle add-on, unclear-link and blank-cell rule claims (not on the rules page), Impress availability (help page is Writer only).

Method: documentation only; no commands were run.
