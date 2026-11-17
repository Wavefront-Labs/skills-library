---
id: computing-software.web-development.vitepress.markdown-anchors-toc-tables-footnotes
name: markdown-anchors-toc-tables-footnotes
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, markdown, header-anchors, custom-anchor, toc, tables, task-lists, footnotes, emoji]
level: intro
status: docs-checked
description: "Use VitePress Markdown basics: custom heading anchors, GitHub tables, task lists, footnotes, emoji and the [[toc]] table of contents."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- **Header anchors** are automatic (`markdown.anchor` configures rendering). Set your own id with a suffix: `# Using custom anchors {#my-anchor}` so the link is `#my-anchor` rather than `#using-custom-anchors`.
- **GitHub-style tables** with alignment: `| a | b |` header and `| --- | :---: | ---: |` delimiter row (left, center, right).
- **Task lists:** `- [ ] todo` and `- [x] done`.
- **Footnotes:** `Text[^1]` with `[^1]: Definition (may contain **markdown**)`, and inline footnotes `^[inline text]`; definitions render at page end.
- **Emoji shortcodes:** `:tada: :100:`; the full list comes from the mdit-plugins emoji dataset.
- **Table of contents:** put `[[toc]]` in the page. Configure with `markdown.toc`, for example `toc: { level: [1, 2] }`, which uses `@mdit-vue/plugin-toc` options.
- **Frontmatter** is supported at the top of any page (YAML between `---` lines).

Math equations are opt-in: install `markdown-it-mathjax3` and set `markdown.math` to `true` (see the math skill).

External and internal link behaviour lives in the linking skill; code features have their own skills.

Verify: build the page and click a heading anchor; the URL fragment should match your custom id.

## Checked

Read the header anchors, tables, task lists, footnotes, emoji, table of contents, math and advanced configuration sections of the markdown guide. Confirmed the custom anchor syntax, `markdown.anchor`, `markdown.toc` with `toc: { level: [1, 2] }` and `@mdit-vue/plugin-toc`, and the math opt-in. Removed the stable-ids remark and the claim about literal dollar signs, which the guide does not state.

Method: docs-only read of cited pages, 2026-11-08
