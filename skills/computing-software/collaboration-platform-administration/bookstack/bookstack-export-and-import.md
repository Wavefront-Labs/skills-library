---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-export-and-import
name: bookstack-export-and-import
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, export, import, portable-zip, pdf, markdown, html-export, content-migration]
level: intro
status: docs-checked
description: "Export BookStack content as HTML, PDF, text, Markdown or portable ZIP, import portable ZIPs, and why exports are not a backup."
sources: ["https://www.bookstackapp.com/docs/user/export-import/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack export and import

Export needs the "Export content" permission. Formats:

- Contained web file (.html): embeds images where possible; usually the most faithful.
- PDF: may miss features compared with the screen.
- Plain text (.txt).
- Markdown (.md): original source for pages written in the Markdown editor; other pages are converted and may keep some HTML.
- Portable ZIP (.zip): data, attachments and images, re-importable into BookStack.

Browser printing and the REST API are other routes.

Import needs the "Import content" permission and supports only the Portable ZIP. Use the Import action on the Books page or the `/import` path; you see a preview before running, and the uploaded ZIP is deleted afterwards. Exports and imports are not meant for backup or restore: use the database and files backup procedure instead.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) user/export-import/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.
