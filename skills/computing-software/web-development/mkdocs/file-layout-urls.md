---
id: computing-software.web-development.mkdocs.file-layout-urls
name: file-layout-urls
category: computing-software
field: web-development
product: mkdocs
tags: [file-layout, directory-urls, docs-dir, page-urls]
level: intro
status: docs-checked
description: "How the layout of Markdown files under docs maps to page URLs in a MkDocs site, including nested directories and non-Markdown files."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Source Markdown lives in the docs directory (default `docs/`, beside `mkdocs.yml`). The file layout determines URLs:

```text
docs/
    index.md                          ->  /
    about.md                          ->  /about/
    user-guide/getting-started.md     ->  /user-guide/getting-started/
    license.md                        ->  /license/
```

Rules:
- By convention the homepage is `index.md`.
- Every Markdown file in `docs_dir` is rendered into the site regardless of settings (unless excluded with `exclude_docs`).
- Files that are not Markdown (judged by extension) are copied to the site unaltered; this is how images and a `CNAME` get published.
- Names starting with a dot are ignored unless `exclude_docs` overrides that.

Related: `source-extensions-dotfiles`, `index-readme-pages`, `use-directory-urls`.

## Checked

2026-11-04. Confirmed against the MkDocs user guide page "Writing your docs" (File layout section): default `docs` directory beside `mkdocs.yml`, URL mapping examples, non-Markdown files copied unaltered, dot-files ignored unless `exclude_docs` overrides. Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
