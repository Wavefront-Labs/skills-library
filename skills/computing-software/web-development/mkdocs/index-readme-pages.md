---
id: computing-software.web-development.mkdocs.index-readme-pages
name: index-readme-pages
category: computing-software
field: web-development
product: mkdocs
tags: [index-pages, readme-md, index-md, repository-browsing]
level: practitioner
status: docs-checked
description: "Name a directory's index page index.md or README.md in MkDocs; README.md is rendered to index.html and loses to index.md when both exist."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Web servers usually return `index.html` for a directory request, so MkDocs renders `index.md` to `index.html`.

Repository hosts display `README.md` when browsing a directory, so MkDocs also accepts `README.md` as the index page. When the site is rendered the file is renamed to `index.html`, so your source stays friendly on the repo host and the server still gets a proper index.

Rule: if both `index.md` and `README.md` exist in one directory, `index.md` is used and `README.md` is ignored.

```text
docs/
    README.md        # becomes /index.html
    guide/
        README.md    # becomes /guide/index.html
        index.md     # wins over README.md here if both are present
```

Also: automatic navigation (no `nav` set) always lists index files first within a sub-section.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Index pages; Configure Pages and Navigation). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
