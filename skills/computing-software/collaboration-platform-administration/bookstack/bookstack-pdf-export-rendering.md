---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-pdf-export-rendering
name: bookstack-pdf-export-rendering
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, pdf-export, dompdf, export-pdf-command, weasyprint, wkhtmltopdf, export-page-size]
level: advanced
status: docs-checked
description: "Choose a BookStack PDF renderer: default dompdf, an external EXPORT_PDF_COMMAND such as weasyprint with timeout, deprecated wkhtmltopdf, and page size."
sources: ["https://www.bookstackapp.com/docs/admin/pdf-rendering/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack PDF rendering

- dompdf is the default: nothing to install, limited rendering.
- `EXPORT_PDF_COMMAND` runs an external renderer; the placeholders `{input_html_path}` and `{output_pdf_path}` are substituted. `EXPORT_PDF_COMMAND_TIMEOUT` is in seconds (default 15).
- wkhtmltopdf is deprecated as of v24.05. It is used if a `wkhtmltopdf` binary sits in the BookStack base folder or `WKHTMLTOPDF` points to it, and it requires `ALLOW_UNTRUSTED_SERVER_FETCHING=true`; otherwise dompdf is used.
- `EXPORT_PAGE_SIZE=letter` for US Letter (default A4).

```
EXPORT_PDF_COMMAND="weasyprint {input_html_path} {output_pdf_path}"
```
The docs warn this direct weasyprint use is not considered secure because of possible filesystem and network access. The safer documented pattern runs weasyprint in a container (the docs use the `4teamwork/weasyprint` image behind a Caddy proxy on port 3000) and has BookStack call it with curl, which must then be installed on the host.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/pdf-rendering/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: a closing tip about raising the timeout.
Method: documentation only; no commands were run.
