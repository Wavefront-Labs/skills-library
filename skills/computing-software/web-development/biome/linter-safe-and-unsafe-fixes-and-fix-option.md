---
id: computing-software.web-development.biome.linter-safe-and-unsafe-fixes-and-fix-option
name: linter-safe-and-unsafe-fixes-and-fix-option
category: computing-software
field: web-development
product: biome
tags: [biome, safe-fixes, unsafe-fixes, write-unsafe, fix-option, sourcefixall, code-fix, lint-write]
level: practitioner
status: docs-checked
description: "Apply safe fixes with --write, unsafe with --write --unsafe, use source.fixAll.biome on save, and reclassify a rule's fix with the fix option."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Many rules ship a code fix. Biome distinguishes two kinds.

**Safe fixes** are guaranteed not to change the semantics of your code and can be applied without review: `biome lint --write ./src`. In LSP-compatible editors apply them on save with the code action `source.fixAll.biome`.

**Unsafe fixes** may change program semantics, so review them: `biome lint --write --unsafe ./src`. Editors cannot apply all unsafe fixes on save, since silently changing semantics on save is undesirable; you can review and apply a single fix instead.

**Reclassify with `fix`.** In the rule config, `fix` takes `none` (no fix emitted), `safe` or `unsafe`:

```jsonc
{ "linter": { "rules": {
  "correctness": { "noUnusedVariables": { "level": "error", "fix": "none" } },
  "style": {
    "useConst": { "level": "warn", "fix": "unsafe" },
    "useTemplate": { "level": "warn", "fix": "safe" }
  } } } }
```

**Why is a fix unsafe even when it looks safe?** The documented reasons: the rule and fix are still under heavy development; the fix can change program semantics so the user must opt in; or the fix harms the typing/saving experience. Example: `noUnusedVariables` prefixes unused variables with `_`, which is disruptive while typing and saving. If none of the reasons apply the team may have forgotten to mark it safe; open an issue or PR.

Editor integration: for each diagnostic the editor offers the code fix (if the rule has one, safe or unsafe), an inline suppression and a top-level suppression.

## Checked

2026-11-08. Read the linter index page in full. Unchanged: safe versus unsafe fixes, --write and --unsafe, source.fixAll.biome, the fix option values, the FAQ reasons and editor actions. Removed: the invented Verify step.

Method: documentation only; no commands were run.
