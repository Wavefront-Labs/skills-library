---
id: computing-software.software-engineering.dart.dart-list-map-set-spread-collection-if
name: dart-list-map-set-spread-collection-if
category: computing-software
field: software-engineering
product: dart
tags: [dart, list-map-set-spread-collection-if]
level: practitioner
status: docs-checked
description: "Build Dart lists, maps and sets with spread, null-aware spread, collection if and for."
sources: ["https://dart.dev/language/collections", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Collection literals
- `[...a, if (x) 1, for (var i in b) i * 2]`; `{...m1, 'k': v}`; `{1, 2}` is a Set, `{}` is a Map.
- `const []` is a compile-time constant list.
- `map.putIfAbsent(key, () => value)` assigns only when the key is absent.
Verify: `var x = {};` is a Map, `<String>{}` is a Set.

## Checked

Date: 2026-11-02. Confirmed on the Collections page: spread, null-aware spread, collection if and for, set vs map `{}`, const lists; Core libraries page: `putIfAbsent`. Removed as not stated in the pages read: `List.unmodifiable`, `List.generate`, `List.filled`, `map.update`, `Map.fromEntries`, `entries` and the ConcurrentModificationError claim.

Method: documentation only; no commands were run.
