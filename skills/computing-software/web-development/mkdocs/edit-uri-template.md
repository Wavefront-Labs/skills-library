---
id: computing-software.web-development.mkdocs.edit-uri-template
name: edit-uri-template
category: computing-software
field: web-development
product: mkdocs
tags: [edit-uri-template, edit-links, path-noext, percent-encoding]
level: advanced
status: docs-checked
description: "Use edit_uri_template for edit links that need custom path placement, with the path, path_noext and !q fields; ready examples for GitHub Wiki and Bitbucket."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`edit_uri_template` is the flexible variant of `edit_uri`; the two are mutually exclusive (do not set both). These are equivalent:

```yaml
edit_uri: 'blob/main/docs/'
edit_uri_template: 'blob/main/docs/{path}'
```

It is a Python format string with only these fields:
- `{path}` e.g. `foo/bar.md`
- `{path_noext}` e.g. `foo/bar`
- conversion flag `!q` percent-encodes: `{path!q}` gives `foo%2Fbar.md`

Examples from the docs:

```yaml
# GitHub Wiki
repo_url: 'https://github.com/project/repo/wiki'
edit_uri_template: '{path_noext}/_edit'

# Bitbucket editor
repo_url: 'https://bitbucket.org/project/repo/'
edit_uri_template: 'src/master/docs/{path}?mode=edit'

# GitLab Static Site Editor
repo_url: 'https://gitlab.com/project/repo'
edit_uri_template: '-/sse/master/docs%2F{path!q}'
```

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (edit_uri_template): mutual exclusion with `edit_uri`, the `{path}`, `{path_noext}` and `!q` fields, and the three examples. Removed: a generic verify line.

Method: documentation only; no commands were run.
