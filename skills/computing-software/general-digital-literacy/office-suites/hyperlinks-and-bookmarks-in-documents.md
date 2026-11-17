---
id: computing-software.general-digital-literacy.office-suites.hyperlinks-and-bookmarks-in-documents
name: hyperlinks-and-bookmarks-in-documents
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, wp-structure, document-hyperlinks, bookmarks, internal-links]
level: intro
status: docs-checked
description: "Link text to a web page, an email address, a heading or a bookmark inside the same Word or Google Doc, and fix links that break after export to PDF."
sources:
  - https://support.microsoft.com/en-us/word/add-or-delete-bookmarks-in-a-word-document-or-outlook-message
  - https://support.microsoft.com/en-us/word/create-a-cross-reference
  - https://support.microsoft.com/en-us/office/save-or-convert-to-pdf-or-xps-in-office-desktop-apps-d85416c5-7d77-4fd6-a216-6f4bf7c7c110
  - https://support.microsoft.com/en-us/office/keyboard-shortcuts-in-word-95ef89dd-7142-4b50-afb2-f762f663ceb2
  - https://support.google.com/docs/answer/45893
  - https://support.google.com/docs/answer/116338
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hyperlinks and bookmarks inside documents

## Link to a web page or email
- Select text, **Ctrl+K** (Cmd+K on Mac) in Word and Google Docs. Enter the web address (Docs also
  accepts an email address).
- Remove in Word: right-click › *Remove Hyperlink*; in Docs click the link › Remove (or Change).

## Link to a place in the same document
- **Bookmarks**: select the target, **Insert › Bookmark**. Word: type a name (must start with a letter;
  letters and numbers, no spaces, use `_` between words) › Add. Docs: the bookmark is created at the cursor.
- **Link to it**: Word: right-click the source text › Link › *Place in This Document* › pick a heading
  (built-in heading styles) or bookmark. Docs: Insert › Link › **Bookmarks** › pick one › Apply.
- Jump to a bookmark in Word: `Ctrl+G` › Go to what: Bookmark.
- A table of contents built from heading styles links to each heading automatically.

## Cross-references
- Word **Insert › Cross-reference** inserts a reference to a heading, bookmark, figure or page that
  updates (Ctrl+A, F9) and can be a hyperlink (*Insert as hyperlink*).

## Export to PDF keeping navigation
- Word: File › Save As › PDF › **Options** › *Create bookmarks using*: Headings (or Word Bookmarks) so
  the PDF gets a bookmark pane.

## Gotchas
- Write meaningful link text ("2025 price list"), never "click here".
- Deleting a bookmark leaves links to it pointing nowhere; remove or redirect those hyperlinks.
- Links to files on your own computer break for everyone else; link to a shared cloud copy.

## Verify
- [ ] Every link tested in the document and in the exported PDF.

## Checked
2026-10-27 against Microsoft Support (bookmarks, cross-reference, Save as PDF, Word shortcuts) and Google
Docs Editors Help (links and bookmarks; headings and table of contents). Confirmed: Ctrl+K in both apps,
bookmark naming rules, Place in This Document, Docs Insert › Link › Bookmarks, Ctrl+G Go To, Insert ›
Cross-reference, and Create bookmarks using Headings. Removed unconfirmed claims about Docs heading links,
Print to PDF, Docs PDF download and Word's Show bookmarks option. Method: documentation only; no commands were run.
