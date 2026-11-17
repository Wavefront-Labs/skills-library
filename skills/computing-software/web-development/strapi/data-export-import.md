---
id: computing-software.web-development.strapi.data-export-import
name: data-export-import
category: computing-software
field: web-development
product: strapi
tags: [strapi, strapi-export, strapi-import, backup, archive, encryption]
level: practitioner
status: docs-checked
description: "Back up and restore Strapi project data with strapi export and strapi import, including unencrypted and directory formats."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# strapi export and import

## Export
Default output is a `.tar` compressed with gzip and encrypted with `aes-128-ecb`, named `export_YYYYMMDDHHMMSS` unless you pass `-f`/`--file`. The archive holds `configuration`, `entities`, `links` and `schemas` folders as JSON lines files.

```bash
strapi export
strapi export -f myData
strapi export --no-encrypt
strapi export --format dir --no-encrypt -f my-export
```

`-f myData` produces `myData.tar.gz.enc`. `--no-encrypt --no-compress` generates a plain archive.

## Import
Data must come from another Strapi application. `--file` is required. Accepts `.tar`, `.tar.gz`, `.tar.gz.enc` and unpacked export directories; compression and encryption are detected from the filename for archives.

```bash
strapi import -f your-filepath-and-filename --key my-key
strapi import -f ./my-export
```

`-k`/`--key` supplies the encryption key on the command line instead of a prompt. `--force` skips the confirmation prompt warning that the import deletes existing data.

## Checked

Checked 2026-11-04 against the Strapi CLI page (`strapi export` and `strapi import` sections and option tables). Removed the generic self-check line about the same key, which the page does not state in that form.

Method: documentation only; no commands were run.
