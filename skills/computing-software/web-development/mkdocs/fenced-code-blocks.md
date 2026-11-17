---
id: computing-software.web-development.mkdocs.fenced-code-blocks
name: fenced-code-blocks
category: computing-software
field: web-development
product: mkdocs
tags: [fenced-code-blocks, code-fences, syntax-highlighting, python-markdown]
level: intro
status: docs-checked
description: "Use fenced code blocks in MkDocs pages with an optional language tag, and avoid nesting them in lists or blockquotes."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/mkdocs.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Fenced blocks avoid indentation. Use 3 or more backticks to open and the same number to close; optionally name the language after the opening fence so highlighters know it:

````markdown
```python
def fn():
    pass
```
````

Gotcha: with this extension a fenced block cannot be indented, so it cannot be nested inside list items or blockquotes. The MkDocs project's own `mkdocs.yml` lists `pymdownx.superfences` under `markdown_extensions` (a third-party extension; see its docs).

Syntax highlighting itself is theme-controlled: the built-in themes use highlight.js (`highlightjs`, `hljs_languages` options).

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Fenced code blocks), the "Choosing your theme" options `highlightjs` and `hljs_languages`, and the project `mkdocs.yml` (lists `pymdownx.superfences`). Removed the nesting-a-fence tip and the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
