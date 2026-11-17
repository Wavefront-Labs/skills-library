---
id: computing-software.web-development.docusaurus.doc-pagination
name: doc-pagination
category: computing-software
field: web-development
product: docusaurus
tags: [pagination-next, pagination-prev, pagination-label, next-previous, front-matter]
level: practitioner
status: docs-checked
description: "How Docusaurus builds next and previous doc links from the displayed sidebar, and overriding or disabling them with pagination_next, pagination_prev and pagination_label."
sources:
  - https://raw.githubusercontent.com/facebook/docusaurus/main/website/docs/guides/docs/sidebar/multiple-sidebars.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pagination links at the bottom of a doc come strictly from the sidebar displayed for that doc. No associated sidebar means no pagination. If `displayed_sidebar` names a sidebar that does not contain the doc itself, no pagination is shown either.

The "next" and "previous" docs belong to that sidebar but may display a different one via their own `displayed_sidebar`.

Override per doc with front matter:

```md title="windows.md"
---
pagination_next: getting-started
---
```

Example: with a sidebar `introduction`, a category `installation` (`windows`, `linux`, `macos`), then `getting-started`, the default next link from `windows` is `linux`. Set `pagination_next` to skip ahead.

Disable a link with `pagination_next: null` or `pagination_prev: null`.

The label defaults to the sidebar label; customize how the doc appears in pagination with `pagination_label`.

`ref` sidebar items are ignored when generating pagination, as if you had set `pagination_next` and `pagination_prev` around them.

## Checked

2026-11-04. Read in full against the Docusaurus Using multiple sidebars page (multiple-sidebars.mdx), Generating pagination section: pagination follows the displayed sidebar, no pagination without one or when the sidebar lacks the doc, pagination_next, pagination_prev, null to disable, pagination_label, and ref items ignored all match. Nothing removed.

Method: documentation only; no commands were run.
