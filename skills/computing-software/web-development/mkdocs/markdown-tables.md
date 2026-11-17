---
id: computing-software.web-development.mkdocs.markdown-tables
name: markdown-tables
category: computing-software
field: web-development
product: mkdocs
tags: [tables, markdown-tables, column-alignment, python-markdown]
level: intro
status: docs-checked
description: "Write tables in MkDocs Markdown: header separator row, optional outer pipes, colon alignment, and the blank-line and single-line-cell limits."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `tables` extension adds the popular pipe syntax:

```markdown
| First Header | Second Header | Third Header |
| ------------ | ------------- | ------------ |
| Content Cell | Content Cell  | Content Cell |
```

Leading and trailing pipes are optional. Alignment uses colons in the separator row:

```markdown
First Header | Second Header | Third Header
:----------- |:-------------:| -----------:
Left         | Center        | Right
```

Rules and gotchas:
- A table must be surrounded by blank lines (one before, one after).
- Cells cannot contain block-level elements or multiple lines of text; inline Markdown is fine.
- It suits simple tabular data only.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Tables). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
