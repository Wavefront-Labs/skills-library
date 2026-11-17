---
id: computing-software.systems-network-administration.paperless-ngx.ocr-languages
name: ocr-languages
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, ocr-language, tesseract, paperless-ocr-languages, dateparser, languages]
level: practitioner
status: docs-checked
description: "Set OCR languages with PAPERLESS_OCR_LANGUAGE, install extra Tesseract packs in Docker, and match the date and search language settings."
sources:
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCR languages

## Choose the language
`PAPERLESS_OCR_LANGUAGE` takes Tesseract 3-letter codes and defaults to `eng`. Set it to the language most of your documents are written in. Combine languages with `+`, for example `deu+eng`; Tesseract uses whatever matches best but needs much more CPU time with several languages. A code containing a dash such as `chi-sim` must be written `chi_sim` here.

## Install packs in Docker
The image comes with English, German, Italian, Spanish and French. For others, list them space-separated:
```bash
PAPERLESS_OCR_LANGUAGES=tur ces chi-tra
PAPERLESS_OCR_LANGUAGE=tur
```
The install list uses package-style names (`chi-tra`), which do not always match the language code (`chi_tra`). It defaults to none and must not be used in rootless containers. Languages not installed by default must be listed in `PAPERLESS_OCR_LANGUAGES` for Docker, or installed as Tesseract language packages for bare metal.

## Bare metal
Install the Tesseract language packages yourself, for example `apt-get install -y tesseract-ocr-spa` on Ubuntu or Debian for Spanish. If OCR accuracy is low or the consumer warns `OCR for XX failed, but we're going to stick with what we've got since FORGIVING_OCR is enabled`, you may need to install the Tesseract language files matching your documents.

## Related languages
- `PAPERLESS_DATE_PARSER_LANGUAGES` uses dateparser codes (`en`, `en+de`, locales such as `en-AU`), not the 3-letter Tesseract codes. If unset, Paperless tries to infer it from `PAPERLESS_OCR_LANGUAGE`.
- `PAPERLESS_DATE_ORDER` (default `DMY`) is the date format Paperless expects in your documents; the letters D, M and Y can be shuffled.
- `PAPERLESS_SEARCH_LANGUAGE` sets the stemmer language for the full-text search index, using ISO 639-1 codes (`en`, `de`) or lowercase full names (`english`). Changing it rebuilds the index automatically on next startup. If unset it is inferred from `PAPERLESS_OCR_LANGUAGE`.

## Checked
Date: 2026-11-07
Pages read in full: configuration (docs/configuration.md), troubleshooting (docs/troubleshooting.md).
Corrections: replaced "usually means the language pack is missing" with the troubleshooting wording ("you might need to install"), and gave the exact warning string; added the search-language inference and the DATE_ORDER description.
Method: documentation only; no commands were run.
