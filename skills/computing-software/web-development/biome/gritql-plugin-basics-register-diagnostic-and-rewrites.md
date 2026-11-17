---
id: computing-software.web-development.biome.gritql-plugin-basics-register-diagnostic-and-rewrites
name: gritql-plugin-basics-register-diagnostic-and-rewrites
category: computing-software
field: web-development
product: biome
tags: [biome, gritql-plugin, register-diagnostic, grit-file, fix-kind, rewrite-operator, plugin-severity, object-assign, target-language]
level: practitioner
status: docs-checked
description: "Write a .grit plugin with register_diagnostic (span, message, severity, fix_kind), enable it in config, and add => rewrites applied by --write."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A GritQL plugin lives in a `.grit` file anywhere in the project. Example reporting `Object.assign()`:

```grit
`$fn($args)` where {
    $fn <: `Object.assign`,
    register_diagnostic(
        span = $fn,
        message = "Prefer object spread instead of `Object.assign()`"
    )
}
```

Enable it with `"plugins": ["./path-to-plugin.grit"]`. It runs on all supported files the linter processes and shows in `biome lint` or `biome check` output with category `plugin`. Suppress with `lint/plugin` comments.

**`register_diagnostic()`** is Biome's one extra function beyond Grit's built-ins. Arguments:
- `span` (required): the syntax node to attach to, usually a matched variable.
- `message` (required).
- `severity`: `hint`, `info`, `warn` or `error` (default `error`).
- `fix_kind`: `safe` or `unsafe`, relevant only when the pattern uses the rewrite operator `=>`; default is unsafe.

**Rewrites.**

```grit
`console.log($msg)` as $call where {
    register_diagnostic(span = $call,
        message = "Use console.info instead of console.log.",
        severity = "warn", fix_kind = "safe"),
    $call => `console.info($msg)`
}
```

Without `--write` rewrites are only suggestions. `--write` applies those marked `safe`; `--write --unsafe` also applies unsafe ones; omitted `fix_kind` counts as unsafe.

**Target language.** Snippets default to JavaScript or a super language. Put `language css;` at the top for another target; Biome supports JavaScript, CSS and JSON targets. The docs' CSS example matches `$selector { $props }`, finds `color: $color` inside `$props` and reports it unless the selector matches the regex `\.color-.*`.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
