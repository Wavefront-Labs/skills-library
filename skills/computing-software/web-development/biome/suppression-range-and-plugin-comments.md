---
id: computing-software.web-development.biome.suppression-range-and-plugin-comments
name: suppression-range-and-plugin-comments
category: computing-software
field: web-development
product: biome
tags: [biome, biome-ignore-start, biome-ignore-end, range-suppression, overlapping-ranges, plugin-suppression, lint-plugin, grit-plugin-name]
level: advanced
status: docs-checked
description: "Suppress a range with biome-ignore-start and -end (matching pairs, overlap allowed) and silence linter plugin diagnostics by plugin name."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/analyzer/suppressions.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Range suppressions** disable a rule from the line of the start comment to the line of the end comment. Start with `// biome-ignore-start` and finish with `// biome-ignore-end`:

```js
// biome-ignore-start lint/suspicious/noDoubleEquals: reason
a == b;
c == d;
// biome-ignore-end lint/suspicious/noDoubleEquals: reason
f == g;
```

Lines 2 and 3 are suppressed, `f == g` still raises a diagnostic. Every start needs a matching `biome-ignore-end`.

**Overlap is allowed.** Take this sequence: a bare `debugger;`, then `biome-ignore-start` for `noDebugger`, `debugger;`, `biome-ignore-start` for `noDoubleEquals`, `a == b; c == d;`, `biome-ignore-end` for `noDoubleEquals`, `debugger;`, `f == g;`, and finally `biome-ignore-end` for `noDebugger`. Results from the docs:
- The first `debugger` raises a diagnostic (no suppression covers it).
- `noDebugger` is disabled from the line after its start comment until its own end comment, so the later `debugger` is silent.
- `noDoubleEquals` is disabled only between its own start and end, so `f == g` raises a diagnostic.
Each end comment closes the range of the rule it names.

**Plugin suppressions** silence diagnostics from linter plugins. Use `lint/plugin` for all plugins or `lint/plugin/<plugin-name>` for one, where the name is the plugin file name without `.grit`. For example `// biome-ignore lint/plugin/preferObjectSpread: reason` before `Object.assign({}, foo);` disables output of `preferObjectSpread.grit` for that next line; `// biome-ignore lint/plugin: reason` disables all plugins there.

## Checked

2026-11-08. Read the suppressions page in full. Unchanged: range suppressions, the overlapping example and its results, and plugin suppressions including the .grit file-name rule. Removed: the invented Verify step.

Method: documentation only; no commands were run.
