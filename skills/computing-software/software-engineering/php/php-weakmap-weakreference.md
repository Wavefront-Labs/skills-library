---
id: computing-software.software-engineering.php.php-weakmap-weakreference
name: php-weakmap-weakreference
category: computing-software
field: software-engineering
product: php
tags: [php, weakmap-weakreference, memory]
level: advanced
status: docs-checked
description: "Attach data to objects without extending their lifetime using WeakMap and WeakReference, and why spl_object_id is not a safe cache key."
sources: ["https://www.php.net/manual/en/class.weakmap.php", "https://www.php.net/manual/en/class.weakreference.php", "https://www.php.net/manual/en/function.spl-object-id.php", "https://www.php.net/manual/en/function.gc-collect-cycles.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WeakReference and WeakMap

```php
$cache = new WeakMap();            // keys must be objects
$cache[$entity] = $metadata;
isset($cache[$entity]); count($cache);

$ref = WeakReference::create($obj);
$obj = null;
var_dump($ref->get());             // NULL once the object has been destroyed
```
`WeakMap` implements `ArrayAccess`, `Countable` and `IteratorAggregate`, so it is used like an associative array; if the only remaining reference to an object is a WeakMap key, the object is garbage collected and removed from the map. Its primary use case is caches of data derived from an object. `WeakReference` lets you retain a reference without preventing destruction; the object is destroyed when its refcount drops to zero, and `get()` then returns `null`.

## Gotchas
- `spl_object_id()` is unique only for the lifetime of the object; once destroyed, the id may be reused for another object, so an array keyed by object id can return wrong hits. A WeakMap avoids this.
- `gc_collect_cycles()` forces collection of existing garbage cycles.

Verify: store an object in a WeakMap, `unset` it, and assert `count($map) === 0`.

## Checked
2026-11-03. Confirmed on the WeakMap, WeakReference, spl_object_id and gc_collect_cycles manual pages. Removed (not confirmed): worker-framework names, SplObjectStorage strong-reference remark, memory-limit advice, `gc_status`/`memory_get_usage` tips, `create()` same-instance claim.
Method: documentation only; no commands were run.
