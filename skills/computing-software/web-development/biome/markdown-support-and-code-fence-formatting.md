---
id: computing-software.web-development.biome.markdown-support-and-code-fence-formatting
name: markdown-support-and-code-fence-formatting
category: computing-software
field: web-development
product: biome
tags: [biome, markdown, commonmark, gfm, code-fence, fenced-code-blocks, embedded-formatting]
level: practitioner
status: docs-checked
description: "Biome formats CommonMark and GitHub Flavored Markdown and formats fenced code blocks by treating the info string as a file extension."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/introduction/language-support.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Biome supports CommonMark plus GitHub-Flavored Markdown by default (parsing, formatting and linting are all supported; GritQL and JavaScript plugins are not).

**Fenced code blocks.** Biome treats the info string of a fenced block as a file extension and formats the content accordingly. A block like

````md
```js
function name () {
     return "Lorem ipsum"
}
```
````

is rewritten to `function name() {` with two-space style indentation and a normalised body. If Biome does not recognise the info string, the code block is left unchanged.

**Quoted fenced blocks are intentionally ignored.** A fence inside a blockquote (lines starting with `> `) will not be formatted, and the docs state this will not be supported.

**Related.** Embedded CSS and GraphQL in JavaScript template literals are separate and experimental; see the language support skill.

## Checked

2026-11-08. Read the language-support page in full. Unchanged: CommonMark plus GFM, fenced block formatting by info string, unrecognised info strings left alone, quoted fences ignored. Removed: a sentence about Markdown lint rules and assist actions the page does not state, and the invented Verify step.

Method: documentation only; no commands were run.
