---
id: computing-software.software-engineering.zig.style-naming
name: style-naming
category: computing-software
field: software-engineering
product: zig
tags: [zig, style-naming, zig-fmt-style, style-guide, camelcase-functions, pascalcase-types, snake-case, naming-conventions]
level: practitioner
status: docs-checked
description: "Apply the Zig style guide naming rules: camelCase functions, PascalCase types, snake_case variables, file naming and comment conventions."
sources:
  - https://ziglang.org/documentation/0.15.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Style guide: naming, comments and structure
**Goal:** match what the std library and community code do.

From the Style Guide in the Zig language reference (a rule of thumb; follow established conventions such as `ENOENT`):
- Whitespace: 4-space indentation, open braces on the same line, lists longer than 2 items one per line with a trailing comma, aim for 100-column lines.
- A `type` value is `TitleCase` (`const Point = struct {...}`), unless it is a struct with 0 fields never instantiated, which is a namespace and uses `snake_case`.
- A callable returning `type` is `TitleCase` (`fn ArrayList(comptime T: type) type`); any other callable is `camelCase` (`fn readFile()`).
- Everything else is `snake_case` (`const max_size = 100;`, fields, variables).
- Acronyms, initialisms and proper nouns follow the same rules as any other word, even two-letter ones (`XmlParser`, `xml_document`, `readU32Be`).
- File names: a file with top-level fields is `TitleCase.zig`; otherwise `snake_case.zig`. Directory names are `snake_case`.
- Doc comments: omit what the name already says; use the word "assume" for invariants whose violation is unchecked illegal behavior.

## Gotchas
- Names that are not valid identifiers or overlap a keyword use the `@"..."` syntax.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Style Guide section (Whitespace, Names, Examples, Doc Comment Guidance) and the Identifiers text on `@""` in the language reference. Removed: error-name, namespace-repetition, annotation, file-order, linter and ZLS claims.

Method: documentation only; no commands were run.

## Self-check
Check a sample file against the Names rules above: types TitleCase, callables camelCase, everything else snake_case.
