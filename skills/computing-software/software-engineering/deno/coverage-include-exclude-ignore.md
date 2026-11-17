---
id: computing-software.software-engineering.deno.coverage-include-exclude-ignore
name: coverage-include-exclude-ignore
category: computing-software
field: software-engineering
product: deno
tags: [coverage, include, exclude, deno-coverage-ignore, regex, report-filtering]
level: advanced
status: docs-checked
description: "Control which files appear in a Deno coverage report with --include/--exclude regexes and exclude lines or files with deno-coverage-ignore comments."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/test/coverage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the report includes local code and its imports (URLs matching `^file:`) and excludes anything with `test.js`, `test.mjs`, `test.ts`, `test.jsx` or `test.tsx` in its name. A file appears only if it matches the include pattern and not the exclude pattern. Adjust with regexes:

```sh
# Report on main.ts only
deno coverage --include="main.ts" coverage/

# Also include remote modules fetched over https
deno coverage --include="^file:|https:" coverage/
```

Mark intentionally untested code (platform fallbacks, debug helpers, an `import.meta.main` block) with ignore comments; it is treated as blank lines:

```ts
// deno-coverage-ignore
console.log("this single line is ignored");

// deno-coverage-ignore-start
if (import.meta.main) {
  Deno.serve(handler);
}
// deno-coverage-ignore-stop
```

Put `// deno-coverage-ignore-file` at the top of a file to drop it from the report. Every `-start` needs a matching `-stop`, and ranges cannot be nested.

## Checked

2026-11-04. Confirmed against docs runtime/test/coverage.md: default include/exclude patterns, --include/--exclude examples, deno-coverage-ignore comment forms and rules.

Method: documentation only; no commands were run.
