---
id: computing-software.software-engineering.php.php-spl-structures
name: php-spl-structures
category: computing-software
field: software-engineering
product: php
tags: [php, php-arrays, spl-structures]
level: advanced
status: docs-checked
description: "Know the SPL data structure classes (SplStack, SplQueue, heaps, SplPriorityQueue, SplObjectStorage, SplFixedArray) and WeakMap, and measure before replacing arrays."
sources: ["https://www.php.net/manual/en/spl.datastructures.php", "https://www.php.net/manual/en/class.splobjectstorage.php", "https://www.php.net/manual/en/class.splfixedarray.php", "https://www.php.net/manual/en/class.weakmap.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SPL data structures
- The SPL data structures section documents `SplDoublyLinkedList` and its subclasses `SplQueue` and `SplStack`, the heaps (`SplMinHeap`, `SplMaxHeap`), `SplPriorityQueue`, `SplFixedArray` and `SplObjectStorage`.
- `SplObjectStorage` implements `Countable`, `SeekableIterator`, `Serializable` and `ArrayAccess`, so it maps objects to data.
- `WeakMap` (PHP 8.0) is the cache keyed by object that does not keep its keys alive; see the weakmap skill.
- Plain arrays cover most needs; benchmark with realistic sizes before switching to a specialised structure.

Verify: write a micro-benchmark with your real data sizes before adopting a structure for speed or memory.

## Checked
2026-11-03. Confirmed on the SPL data structures, SplObjectStorage, SplFixedArray, SplQueue/SplStack, heap and WeakMap manual pages (class names and interfaces). Removed: claims about memory savings and copy-on-write.
Method: documentation only; no commands were run.
