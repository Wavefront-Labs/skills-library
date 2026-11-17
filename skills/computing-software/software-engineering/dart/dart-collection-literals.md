---
id: computing-software.software-engineering.dart.dart-collection-literals
name: dart-collection-literals
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-collections, collection-literals]
level: intro
status: docs-checked
description: "Build collections with literals, spread, collection if and for and know mutability rules."
sources: ["https://dart.dev/language/collections", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List, Set, Map, spread and collection if/for
- `var l = <int>[1, 2]; var s = <int>{1}; var m = <String, int>{'a': 1};` (`{}` is a Map).
- `[...a, if (x) 1, for (var i in b) i * 2]`; `...?` null-aware spread.
- `const [1, 2]` is a compile-time constant list.
- `map.putIfAbsent(key, () => value)` assigns only when the key is absent.
Verify: `var x = {};` is a Map, `<String>{}` is a Set.

## Checked

Date: 2026-11-02. Confirmed on the Collections page: list, set and map literals, `{}` defaults to Map, spread and null-aware spread, collection if and for, const lists; Core libraries page: `putIfAbsent`. Removed as not stated in the pages read: `List.unmodifiable`, `toList(growable: false)`, `Map.fromEntries`, `entries`/`update`, the LinkedHashMap default and the UnsupportedError check.

Method: documentation only; no commands were run.
