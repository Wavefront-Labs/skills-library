---
id: computing-software.software-engineering.dart.dart-imports-exports
name: dart-imports-exports
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-libraries-imports, imports-exports]
level: practitioner
status: docs-checked
description: "Manage imports with prefixes, show/hide, deferred loading and library-private names."
sources: ["https://dart.dev/language/libraries", "https://dart.dev/tools/pub/create-packages", "https://dart.dev/tools/linter-rules/implementation_imports", "https://dart.dev/libraries/dart-io"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# import, export, show, hide, deferred and part
- `import 'package:foo/foo.dart' as foo;` with prefix; `show`/`hide` combinators; `export 'src/a.dart' show A;` to curate a public API from a file directly under `lib/`.
- Identifiers starting with `_` are private to the library; every Dart file plus its parts is a library.
- Files in `lib/src/` are private by convention: import them only from within the same package, never from another package's `src`.
- `dart:io` cannot be used by web apps. Conditional imports and exports check `dart.library.<name>` keys, which are true when the library is available on the platform: `export 'src/hw_none.dart' if (dart.library.io) 'src/hw_io.dart' if (dart.library.js_interop) 'src/hw_web.dart';` (use `import` the same way). All variants must implement the same API.
- `import '...' deferred as x;` then `await x.loadLibrary()` for lazy loading; it is supported for web only (not other `dart` tool targets). Constants and types of a deferred library cannot be used in the importing file, and calling `loadLibrary()` repeatedly loads once.
- `part`/`part of` split a library across files; the Dart team does not recommend parts, even for generated code, and prefers small libraries.

Verify: the `implementation_imports` lint (enable it in `analysis_options.yaml`) flags imports of another package's `lib/src`.

## Checked

Checked 2026-11-08 against https://dart.dev/language/libraries, https://dart.dev/tools/pub/create-packages, the implementation_imports linter rule page and the dart:io page (web restriction), each read for the cited sections. Corrected: dart.library.html example replaced by the documented dart.library.io / dart.library.js_interop form; deferred loading limits added; the previous claim that `dart analyze` reports implementation_imports by default was replaced by the lint-enabling statement.

Method: documentation only; no commands were run.
