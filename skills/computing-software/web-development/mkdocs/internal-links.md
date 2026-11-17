---
id: computing-software.web-development.mkdocs.internal-links
name: internal-links
category: computing-software
field: web-development
product: mkdocs
tags: [internal-links, relative-links, anchors, raw-html-links]
level: practitioner
status: docs-checked
description: "Link between MkDocs pages with relative Markdown paths to .md files and anchors; why absolute paths and raw HTML links are not converted."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/writing-your-docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use ordinary Markdown links with the relative path to the source `.md` file; the build turns them into links to the HTML page:

```markdown
Please see the [project license](license.md) for details.
Please see the [project license](../about/license.md) for details.
Please see the [project license](about.md#license) for details.
```

Anchors come from headers (toc extension): text lowercased, disallowed characters including whitespace become dashes, consecutive dashes collapse to one.

Gotchas:
- Absolute paths are not officially supported: they are not modified, so they may work locally and break once deployed. (Since 1.6 you can opt in to `validation.links.absolute_links: relative_to_docs`.)
- Raw HTML is ignored by the Markdown parser, so links inside raw HTML are neither validated nor converted; write them correctly for the rendered output yourself.

## Checked

2026-11-04. Confirmed against the MkDocs user guide "Writing your docs" (Internal links; Linking from raw HTML) and "Configuration" (validation of absolute links, new in 1.6). Removed the Verify line, which the pages do not state.
Method: documentation only; no commands were run.
