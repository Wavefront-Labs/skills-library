---
id: computing-software.software-engineering.dart.dart-dart-doc-generation
name: dart-dart-doc-generation
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-docs-tooling, dart-doc-generation]
level: practitioner
status: docs-checked
description: "Generate API docs with dart doc and write doc comments, library docs and code examples."
sources: ["https://dart.dev/tools/dart-doc", "https://dart.dev/effective-dart/documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dart doc and library-level docs
- `dart doc .` writes HTML to `doc/api` by default; `--output=<dir>` changes the directory; `dart doc --dry-run .` reports errors and warnings without saving docs. Options go in `dartdoc_options.yaml` at the package root.
- Generated docs must be served over HTTP to be viewed; only public libraries and members are documented.
- Doc comments use `///`. A library-level comment goes above the `library;` directive. Square brackets (`[name]`) link to API names.
- Code in doc comments: fenced blocks tagged `dart`.
- pub.dev generates and hosts docs for an uploaded package's public libraries.
Verify: `dart doc --dry-run .` emits no warnings.

## Checked
2026-11-03. Confirmed against dart.dev tools/dart-doc (output dir, `--output`, `--dry-run`, dartdoc_options.yaml, HTTP serving, public libraries, pub.dev hosting) and effective-dart/documentation (`///`, `library;`, brackets, fenced dart blocks). Removed: `--validate-links`, `{@template}`/`{@macro}` (not on the pages read).
Method: documentation only; no commands were run.
