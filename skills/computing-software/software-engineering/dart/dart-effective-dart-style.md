---
id: computing-software.software-engineering.dart.dart-effective-dart-style
name: dart-effective-dart-style
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-style, effective-dart-style]
level: practitioner
status: docs-checked
description: "Apply Effective Dart naming, import ordering and /// documentation conventions."
sources: ["https://dart.dev/effective-dart/style", "https://dart.dev/effective-dart/documentation", "https://dart.dev/effective-dart/usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming, formatting and doc comments
- Types and extensions `UpperCamelCase`; packages, directories, source files and import prefixes `lowercase_with_underscores`; other identifiers `lowerCamelCase`. In new code constants, including enum values, are `lowerCamelCase`; `SCREAMING_CAPS` is acceptable only to match existing code.
- Capitalise acronyms and abbreviations longer than two letters like words (`HttpClient`).
- Order imports: `dart:` first, then `package:`, then relative; sort each section alphabetically. Prefer relative import paths within a package (lint `prefer_relative_imports`).
- Doc comments use `///`. Put a one-sentence summary first, then a blank line, then details; refer to in-scope identifiers with square brackets (`[name]`).
- `dart doc` generates HTML documentation from doc comments.
Verify: `dart analyze` with your chosen lint set passes.

## Checked
2026-11-03. Confirmed against dart.dev effective-dart/style (naming, constants, acronyms, import order), effective-dart/usage (`prefer_relative_imports`) and effective-dart/documentation (`///`, first-sentence paragraph, square brackets, dart doc). Removed: the unqualified "not SCREAMING_CASE" wording.
Method: documentation only; no commands were run.
