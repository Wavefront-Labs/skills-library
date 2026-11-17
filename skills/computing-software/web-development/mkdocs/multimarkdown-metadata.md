---
id: computing-software.web-development.mkdocs.multimarkdown-metadata
name: multimarkdown-metadata
category: computing-software
field: web-development
product: mkdocs
tags: [multimarkdown, meta-data, page-meta, front-matter]
level: practitioner
status: docs-checked
description: "Write MultiMarkdown style page meta-data in MkDocs: keyword lines, indented continuation, blank line to end, and why delimiters switch to YAML mode."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
MultiMarkdown meta-data is a block of keyword lines at the very start of the file, with no `---` delimiters:

```text
Title:   My Document
Summary: A brief description of my document.
Authors: Waylan Limberg
         Tom Christie
Date:    January 23, 2018
blank-value:
some_url: https://example.com

This is the first paragraph of the document.
```

Rules:
- Keywords are case-insensitive; letters, numbers, underscores and dashes; must end with a colon. Values may be blank.
- A line indented by 4 or more spaces continues the previous keyword's value; lines are joined into one string.
- The first blank line ends the meta-data, so the first line of the document must not be blank.
- MkDocs uses the presence of `---`/`...` delimiters to choose YAML mode. If delimiters are present but the content is not valid YAML, it does not fall back to MultiMarkdown parsing.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (MultiMarkdown Style Meta-Data). Removed the Verify line, which the page does not state.
Method: documentation only; no commands were run.
