---
id: computing-software.search-and-information-retrieval.apache-solr.json-update-commands
name: json-update-commands
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [json-updates, json-update, update-json-docs, update-commands, commitwithin, update-handler]
level: intro
status: docs-checked
description: "Send documents and commands to the Solr /update handler as JSON: one doc via /update/json/docs, arrays of docs, and add, delete, commit commands with commitWithin and overwrite."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/indexing-with-update-handlers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# json-update-commands

`/update` is a unified `UpdateRequestHandler` that picks a loader from the Content-Type; it accepts JSON, XML, CSV and javabin. Use `Content-Type: application/json`.

Three JSON forms:
1. One document: POST the object to `/update/json/docs`.
2. Many documents: POST a JSON array of objects to `/update`.
3. Commands: POST an object holding `add`, `delete`, `commit` and `optimize` keys. A single top-level document sent to `/update` needs `json.command=false`.

Command options:
- `add` with `commitWithin` (milliseconds) and `overwrite` (false keeps duplicates by id).
- `delete` by `id` or by `query`.
- `commit: {}` and `optimize: {"waitSearcher":false}`.

Append `?commit=true` to commit with the request. Pre-process documents with update request processors, which run before documents are checked against the schema.

Arbitrary JSON structures need the mapping parameters of `/update/json/docs`.

## Checked

2026-11-04. Confirmed against the Solr Reference Guide Indexing with Update Handlers page: the unified handler and its Content-Type loaders, `/update/json/docs`, the three JSON forms and `json.command=false`, `commitWithin`, `overwrite`, `optimize` with `waitSearcher`, URL-level `commit`, and update request processors running before the schema check. Nothing removed.

Method: documentation only; no commands were run.
