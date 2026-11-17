---
id: computing-software.web-development.mkdocs.docs-dir-site-dir
name: docs-dir-site-dir
category: computing-software
field: web-development
product: mkdocs
tags: [docs-dir, site-dir, build-directories, gitignore]
level: intro
status: docs-checked
description: "Change where MkDocs reads Markdown (docs_dir) and writes HTML (site_dir); relative paths resolve against the config file directory."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
docs_dir: docs      # default
site_dir: site      # default
```

- `docs_dir`: directory with the source Markdown. A relative value resolves relative to the directory containing the config file; an absolute path from the filesystem root also works.
- `site_dir`: where HTML and other output files are created, resolved the same way.

Keep build output out of version control; with git add to `.gitignore`:

```text
site/
```

(Adjust the line if you change `site_dir`.)

Related: `nav` paths and `exclude_docs` patterns are relative to `docs_dir`.

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (docs_dir, site_dir, nav, exclude_docs): defaults `docs` and `site`, relative paths resolve against the config file directory, absolute paths allowed, and the `.gitignore` advice. Removed: a claim that a custom theme directory must not be inside `docs_dir` (not on the page) and a generic verify line.

Method: documentation only; no commands were run.
