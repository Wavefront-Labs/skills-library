---
id: computing-software.systems-network-administration.audiobookshelf.upload-feature-behaviour
name: upload-feature-behaviour
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [upload, library-structure, auto-fetch-metadata, folders, books]
level: practitioner
status: docs-checked
description: "Use the Audiobookshelf upload feature correctly: library and folder choice, Auto Fetch Metadata scope, and multi-file book rules."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/uploading.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/reverse-proxy/1.nginx-proxy-setup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The built-in upload adds books while ensuring files follow the correct library structure of one book per folder. Choose the library and, within it, the target folder before uploading.

**Auto Fetch Metadata:** tick it and pick a provider to match the books. It only fetches metadata for the **directory structure**, keeping author and series naming consistent. It does not add that metadata to the books. After adding a book, manually trigger a match; depending on your metadata priority this adds only the series and author.

**Multiple files:**

- Several files added together upload as separate books.
- To upload one book made of multiple files, upload the entire folder containing its files.
- Non-audio book files (for example e-books) are always grouped into a single book, even if uploaded separately. Add them directly to the file system or upload them one by one.

Large uploads through a reverse proxy need a raised body limit; NGINX uses `client_max_body_size 10240M` in the docs example to prevent 413 errors.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Uploading page and the NGINX reverse proxy page.

Method: documentation only; no commands were run.
