---
id: computing-software.search-and-information-retrieval.apache-solr.bin-solr-post
name: bin-solr-post
category: computing-software
field: search-and-information-retrieval
product: apache-solr
tags: [post-tool, bin-solr-post, solr-cli, csv-import, web-crawl]
level: intro
status: docs-checked
description: "Load files into Solr with bin/solr post: files, args, stdin and web modes, filetypes, CSV params, credentials and dry runs. Meant for exploration, not production indexing."
sources:
  - https://solr.apache.org/guide/solr/latest/indexing-guide/post-command.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bin-solr-post

`bin/solr post` posts content to Solr. The guide says it is for new users exploring Solr and is not a robust production indexing solution.

Target: `--solr-url` (default `http://localhost:8983`) with `-c`/`--name` for the collection.

Modes (`--mode`): `files` (default, crawls local directories), `web`, `args` (positional arguments) and `stdin`.

Useful options:
- `-ft`/`--filetypes`: default list includes xml, json, jsonl, csv, pdf, doc(x), html, txt. Other extensions are skipped with a warning unless `--type` is set.
- `-t`/`--type`: force a content type, for example `text/csv` for a tab-separated file together with `--params "separator=%09"`.
- `--params`: URL-encoded pass-through to the update request.
- `--skip-commit`, `-o` (optimize at end), `--dry-run` (files mode only), `--verbose`.
- `-u user:password` for Basic auth.
- `-r` and `--delay` for web crawl depth and wait.

Rich files such as PDFs need a configured Tika Server.

## Checked

2026-11-04. Confirmed against the Post Tool page: usage options, modes, filetypes behaviour, `--type` with `--params "separator=%09"`, Tika Server note, not-for-production note. Nothing removed.

Method: documentation only; no commands were run.
