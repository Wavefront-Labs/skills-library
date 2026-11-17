---
id: computing-software.search-and-information-retrieval.apache-solr.solr-cell-tika
name: solr-cell-tika
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [solr-cell, tika-server, extracting-handler, rich-documents, update-extract]
level: advanced
status: docs-checked
description: "Index PDFs and Word files with Solr Cell: ExtractingRequestHandler delegates to an external Tika Server; set tikaserver.url, use literal., fmap., uprefix, extractOnly."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/indexing-with-tika.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# solr-cell-tika

Solr Cell is the `ExtractingRequestHandler` at `/update/extract`. It calls an external Apache Tika Server rather than embedding Tika, so a parser crash does not take Solr down.

Configure the handler with the required `tikaserver.url`, pointing at your Tika Server (port 9998 in the guide's example, which starts one with Docker).

Tika detects the file type; force it with `stream.type`. Tika also emits metadata such as dc:title and dc:author.

Parameters:
- `literal.fieldname`: set a field value for each document; `literalsOverride` (default true) lets literals win over extracted values.
- `fmap.source_field`: rename an extracted field.
- `uprefix`: prefix for fields not in the schema; `defaultField` for content when there is no match.
- `extractOnly=true`: return extracted content without indexing.
- `capture`, `captureAttr`, `lowernames`, `resource.name`, `commitWithin`.

## Checked

2026-11-04. Confirmed against the Indexing with Tika page: external Tika Server delegation and isolation, `tikaserver.url` and the port 9998 Docker example, `literal.`, `literalsOverride`, `fmap.`, `uprefix`, `extractOnly`. Removed a generic closing line.

Method: documentation only; no commands were run.
