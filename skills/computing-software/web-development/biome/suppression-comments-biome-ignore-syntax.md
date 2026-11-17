---
id: computing-software.web-development.biome.suppression-comments-biome-ignore-syntax
name: suppression-comments-biome-ignore-syntax
category: computing-software
field: web-development
product: biome
tags: [biome, biome-ignore, suppressions, inline-suppression, top-level-suppression, biome-ignore-all, diagnostic-category, suppression-unused, analyzer]
level: practitioner
status: docs-checked
description: "Write biome-ignore comments with category, group, rule and explanation, and use inline and top-level (biome-ignore-all) forms correctly."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/analyzer/suppressions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The analyzer underlies both the linter and assist, and they share one suppression engine: you suppress a lint rule the same way you suppress an assist action. Suppression can cover a line, a range or a whole file, using suppression comments.

**Syntax** (`<explanation>` states why the rule is disabled):

```js
// biome-ignore lint: <explanation>
// biome-ignore assist: <explanation>
// biome-ignore syntax: <explanation>
// biome-ignore lint/suspicious: <explanation>
// biome-ignore lint/suspicious/noDebugger: <explanation>
// biome-ignore lint/suspicious/noDebugger(foo): <explanation>
// biome-ignore lint/plugin: <explanation>
// biome-ignore lint/plugin/<plugin-name>: <explanation>
// biome-ignore-all lint: <explanation>
// biome-ignore-start lint: <explanation>
// biome-ignore-end lint: <explanation>
```

After the keyword comes the category: `lint`, `assist` or `syntax`. It may be followed by a group, or group and rule name, separated by slashes; the more you specify the more targeted the suppression. Some rules accept a value in parentheses, such as `(foo)`; check the rule documentation. If unsure of the category, use the diagnostic category shown on the rule or action page.

**Inline suppression.** Disables the rule for the **next line** only. With `// biome-ignore lint/suspicious/noDebugger: reason` before two `debugger;` lines, the first is silenced and the second still raises a diagnostic.

**Top-level suppression.** Must start with `biome-ignore-all` and sit **at the top of the file**. It disables the rule for the whole file, useful when you do not want a single configuration override for one file (generated files, for example). If it is not at the top it is treated as unused and Biome emits a diagnostic with category `suppression/unused`.

## Checked

2026-11-08. Read the suppressions page in full. Unchanged: the comment syntax list, category/group/rule structure, inline and top-level behaviour and the suppression/unused diagnostic. Reworded the claim that an explanation is required, which the page does not state. Removed: the invented Verify step.

Method: documentation only; no commands were run.
