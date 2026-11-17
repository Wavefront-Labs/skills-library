---
id: computing-software.software-engineering.dart.dart-js-interop-web
name: dart-js-interop-web
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-js-interop, js-interop-web]
level: advanced
status: docs-checked
description: "Interact with browser APIs using package:web and extension types instead of dart:html."
sources: ["https://dart.dev/interop/js-interop/package-web", "https://dart.dev/interop/js-interop/usage", "https://dart.dev/interop/js-interop/js-types", "https://dart.dev/interop/js-interop/mock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# package:web and dart:js_interop
- `package:web` is replacing `dart:html` and the other Dart SDK web libraries as Dart's web interop solution; `dart:html` and `dart:svg` are deprecated and not supported when compiling to Wasm. `package:web` is built on `dart:js_interop`, so it works with dart2wasm, and its members are generated from the Web IDL.
- `dart:js_interop` holds the `@JS()` annotation, JS types (`JSString`, `JSArray`, `JSObject`...), conversion functions and utilities. `@JS('name')` renames or namespaces a declaration; a Dart library name is never used as a JS namespace unless you give a non-empty string.
- Convert with `toJS` (Dart to JS) and `toDart` (JS to Dart), for example `'hi'.toJS`, `jsStr.toDart`, `await jsPromise.toDart`.
- Interop types are extension types: `extension type InteropType(JSObject _) implements JSObject {}`. Because they erase to one runtime representation, `is` checks and `as` casts cannot distinguish JS types at runtime.
- Avoid `dart:js_interop_unsafe` (dynamic property access) where possible; it makes security compliance harder.
- To mock interop types, annotate a Dart class with `@JSExport` and use `createJSInteropWrapper`; extension type members cannot be overridden.
- `dart:io` is not available to web apps.

Verify: the app compiles for the web target without importing `dart:html`.

## Checked

Checked 2026-11-08 against the package:web, usage, JS types and mocking pages of the Dart JS interop docs, and the dart:io page. The pages were read for the cited sections, not every example. Removed (not confirmed): the `@JS('Math.max')` external function example, `@JSExport` as a general-purpose attribute outside mocking, the `webdev serve` and `dart compile js` build instructions, and the `dart test -p chrome` verify step.

Method: documentation only; no commands were run.
