---
id: computing-software.software-engineering.php.php-references-by-ref
name: php-references-by-ref
category: computing-software
field: software-engineering
product: php
tags: [php, references-by-ref, semantics]
level: advanced
status: docs-checked
description: "Understand PHP references: &-params, the foreach by-reference trap with unset, and when to avoid references."
sources: ["https://www.php.net/manual/en/language.references.php", "https://www.php.net/manual/en/language.oop5.references.php", "https://www.php.net/manual/en/language.references.pass.php", "https://www.php.net/manual/en/control-structures.foreach.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# References and by-ref semantics

```php
function addOne(array &$a): void { $a[] = 1; }   // caller sees the change
$x = [];  addOne($x);

$a = 1; $b = &$a; $b = 2;   // $a is now 2

$list = [1, 2, 3];
foreach ($list as &$v) { $v *= 2; }
unset($v);   // break the reference with the last element
```

## The foreach trap
The foreach manual page says the reference of `$value` to the last array element remains after a by-reference foreach loop, and recommends destroying it with `unset()`. Without `unset($v)`, a later `foreach ($list as $v)` writes into the last element on each iteration and corrupts the array. Avoid the problem with `array_map` or an index-based loop (`foreach ($list as $k => $v) { $list[$k] = $v * 2; }`).

## Gotchas
- `unset()` on a reference variable removes that name only; it does not destroy the value other names refer to (the pass-by-reference page demonstrates the effect).
- Prefer returning new values over out-parameters; reserve `&` for APIs that need it.
- The objects-and-references page explains that objects are handled via identifiers rather than PHP references: read it before assuming `&` is needed for objects.

Verify: run the double-foreach example and observe the corrupted last element, then add `unset($v)` and observe the fix.

## Checked
2026-11-03. Confirmed on the foreach, pass-by-reference and references manual pages. Removed (not confirmed on the pages read): the `[2,4,4]` output, copy-on-write explanation, returning references remarks, call-time pass-by-reference removal, `@param-out` and `preg_match` examples, claims about references inside copied arrays.
Method: documentation only; no commands were run.
