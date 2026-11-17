---
id: computing-software.web-development.vitepress.markdown-file-inclusion
name: markdown-file-inclusion
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, markdown-include, include-directive, partials, file-inclusion, region-include, line-range]
level: advanced
status: docs-checked
description: "Reuse Markdown with <!--@@include: path-->, line ranges, regions and heading ids, and include code inside fences."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Include one Markdown file in another, even nested:

```md
## Basics

<!--@@include: ./parts/basics.md-->
```

`@` prefix means the source root (project root unless `srcDir` is configured).

**Line ranges:** `{3,}`, `{,10}`, `{1,10}`.

```md
<!--@@include: ./parts/basics.md{3,}-->
```

**Regions** (VS Code style) using `#name`, combinable with ranges:

```md
<!--@@include: ./parts/basics.md#basic-usage{,2}-->
<!--@@include: ./parts/basics.md#basic-usage{5,}-->
```

where the part file wraps content in `<!-- #region basic-usage -->` ... `<!-- #endregion basic-usage -->`.

**Heading anchors** select a section of the part file together with its sub-headings (the guide's example stops before the next same-level heading): `<!--@@include: ./parts/basics.md#my-base-section-->`. Find the id by clicking the heading anchor in the browser, or define one: `## My Base Section {#custom-id}` and include `#custom-id`.

**Behaviour to know**
- A missing file, region, heading anchor, or out-of-range line selection throws a build error; `markdown.include.silent: true` downgrades to a warning and skips.
- Relative links and images inside included files resolve from the *included* file's location, so partials can link to neighbours wherever they are included; `markdown.include.rebaseRelativeUrls: false` resolves relative to the including page instead.
- Inclusion happens before code blocks are parsed, so it works inside fences: put the directive in a ```js fence with a line range to show part of a code file. Lines are inserted verbatim (indentation preserved); content containing backticks needs a longer outer fence.

Verify: the page shows the included text and the build fails when the target is missing.

## Checked

Read the Markdown File Inclusion section of the markdown guide. Confirmed the include directive, `@` source root, line range forms, regions with ranges, heading-anchor inclusion and custom ids, build-error and `markdown.include.silent` behaviour, `rebaseRelativeUrls`, and inclusion inside fences. Reworded the heading-section rule to what the example shows.

Method: docs-only read of cited pages, 2026-11-08
