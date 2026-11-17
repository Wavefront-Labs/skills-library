---
id: computing-software.web-development.vitepress.code-line-highlight-focus-diff-notations
name: code-line-highlight-focus-diff-notations
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, code-line-highlighting, code-focus, code-diff, code-error-warning, shiki-transformers, line-notation]
level: practitioner
status: docs-checked
description: "Mark lines in code blocks via {4,7-13} ranges and [!code highlight/focus/++/--/error/warning] comments."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/markdown.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Line ranges after the language** highlight lines: single `{4}`, multiple `{4,7,9}`, ranges `{5-8}`, or both `{4,7-13,16,23-27,40}`.

````md
```js{1,4,6-8}
export default { // Highlighted
  data () {
    return {
      msg: `Highlighted!
      This line isn't highlighted,
      but this and the next 2 are.`,
      motd: 'VitePress is awesome',
      lorem: 'ipsum'
    }
  }
}
```
````

**In-line comment notations** (the page's examples put them in a `//` comment at the end of the line):

| Comment | Effect |
|---|---|
| `// [!code highlight]` | highlight this line |
| `// [!code focus]` | focus the line and blur the other parts of the code; `// [!code focus:<lines>]` focuses that number of lines |
| `// [!code --]` / `// [!code ++]` | create a diff of that line while keeping the colours of the code block |
| `// [!code error]` / `// [!code warning]` | colour the line accordingly |

## Checked

2026-11-04. Confirmed against the VitePress Markdown guide (Line Highlighting, Focus, Colored Diffs, Errors and Warnings in Code Blocks). Removed: the advice on when to prefer ranges versus comments, the comparison with a diff fence, the unsupported 'red/green' wording, the rendering-check paragraph and the Verify step.

Method: documentation only; no commands were run.
