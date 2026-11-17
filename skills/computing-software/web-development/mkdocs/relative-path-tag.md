---
id: computing-software.web-development.mkdocs.relative-path-tag
name: relative-path-tag
category: computing-software
field: web-development
product: mkdocs
tags: [relative-tag, snippets, config-dir, docs-dir-variable]
level: advanced
status: docs-checked
description: "Use the !relative YAML tag (1.5+) so Markdown extensions such as pymdownx.snippets resolve paths from the current page, docs_dir or config directory."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`!relative` (new in 1.5) lets config values depend on the Markdown file being processed or on the site root. Known use case: `markdown_extensions` options.

Forms (only `$docs_dir` and `$config_dir` prefixes are recognised):

```yaml
- !relative                              # directory of the current Markdown file
- !relative $docs_dir                    # the docs_dir
- !relative $config_dir                  # directory containing the main mkdocs.yml
- !relative $config_dir/some/child/dir
```

Example, letting snippets include files next to the current page:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      base_path: !relative
```

Gotcha: by default an extension's base path is technically the current working directory, merely assumed to be the mkdocs.yml directory. Prefer the explicit idiom even when you do not want per-page paths:

```yaml
markdown_extensions:
  - pymdownx.snippets:
      base_path: !relative $config_dir
```

## Checked

2026-11-04. Confirmed against the MkDocs configuration guide (Paths relative to the current file or site, new in 1.5): the four forms, only `$docs_dir` and `$config_dir` prefixes, the snippets examples, and the working-directory note. Removed: a verify line the page does not state.

Method: documentation only; no commands were run.
