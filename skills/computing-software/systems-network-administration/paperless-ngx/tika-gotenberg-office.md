---
id: computing-software.systems-network-administration.paperless-ngx.tika-gotenberg-office
name: tika-gotenberg-office
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, tika, gotenberg, office-documents, eml, paperless-tika-enabled]
level: practitioner
status: docs-checked
description: "Enable Office document and .eml consumption with Tika and Gotenberg, and fix 504 Gateway Timeout errors from slow conversions."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
  - "https://docs.paperless-ngx.com/faq/"
  - "https://docs.paperless-ngx.com/setup/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tika and Gotenberg

Tika and Gotenberg let Paperless parse Office documents (the FAQ lists .docx, .doc, .odt, .ppt, .pptx, .odp, .xls, .xlsx, .ods) and are also needed to parse emails (.eml). You must provide a Tika server and a Gotenberg server, configure their endpoints and enable the feature.

## Settings
```bash
PAPERLESS_TIKA_ENABLED=true
PAPERLESS_TIKA_ENDPOINT=http://tika:9998
PAPERLESS_TIKA_GOTENBERG_ENDPOINT=http://gotenberg:3000
```
Defaults: the feature is off, the Tika endpoint is `http://localhost:9998` and the Gotenberg endpoint is `http://localhost:3000`. With Docker Compose, download a compose file with `-tika` in its name (the configuration page points to `docker-compose.sqlite-tika.yml` as a reference) and add all three settings to the webserver environment or `docker-compose.env`.

## Email layout
`PAPERLESS_EMAIL_PARSE_DEFAULT_LAYOUT` is the default layout for emails consumed as documents: 1 text then HTML, 2 HTML then text, 3 HTML only, 4 text only. Mail rules can specify a layout, so this default applies to the default selection and to .eml files consumed by other means.

## 504 Gateway Timeout
```
requests.exceptions.HTTPError: 504 Server Error: Gateway Timeout for url: http://gotenberg:3000/forms/libreoffice/convert
```
Gotenberg has a default timeout of 30 seconds and raises this error when conversion takes longer. Raise it with a Gotenberg command flag in `docker-compose.yml`, keeping the Chromium hardening that stops .eml files loading external content (tracking pixels, JavaScript):
```yaml
command:
  - 'gotenberg'
  - '--chromium-disable-javascript=true'
  - '--chromium-allow-list=^file:///tmp/.*'
  - '--api-timeout=60s'
```
Tika always produces a PDF rendition for display, which counts as the archive file regardless of `PAPERLESS_ARCHIVE_FILE_GENERATION`.

## Checked
Date: 2026-11-07
Pages read in full: configuration, troubleshooting, faq, setup (docs/*.md).
Corrections: removed the claim that the `-tika` compose file "adds both services" (the pages say only that Office support needs a file with `-tika` in its name); used the exact error string from troubleshooting; added setup to sources.
Method: documentation only; no commands were run.
