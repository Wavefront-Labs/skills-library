---
id: computing-software.software-engineering.php.php-iterator-aggregate
name: php-iterator-aggregate
category: computing-software
field: software-engineering
product: php
tags: [php, iterator-aggregate, iterators]
level: practitioner
status: docs-checked
description: "Make objects foreach-able with IteratorAggregate (generator-based) or Iterator, plus SPL iterators and the iterator_to_array key pitfall."
sources: ["https://www.php.net/manual/en/class.iteratoraggregate.php", "https://www.php.net/manual/en/class.iterator.php", "https://www.php.net/manual/en/spl.iterators.php", "https://www.php.net/manual/en/function.iterator-to-array.php", "https://www.php.net/manual/en/function.iterator-count.php", "https://www.php.net/manual/en/class.generator.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterator and IteratorAggregate

Prefer `IteratorAggregate` returning a generator (the IteratorAggregate page shows `yield from $this->data;` inside `getIterator()`): no cursor state to manage.
```php
final class Playlist implements IteratorAggregate, Countable {
    private array $tracks = [];
    public function add(Track $t): void { $this->tracks[] = $t; }
    public function getIterator(): Generator { yield from $this->tracks; }
    public function count(): int { return count($this->tracks); }
}
foreach ($playlist as $i => $track) {}
```
Implement `Iterator` (`current`, `key`, `next`, `rewind`, `valid`) only when you need a stateful cursor.

SPL iterator classes documented on the SPL iterators section include `ArrayIterator`, `LimitIterator`, `CachingIterator`, `CallbackFilterIterator`, `RecursiveIteratorIterator`, `AppendIterator` and `MultipleIterator`. Helpers: `iterator_to_array()`, `iterator_count()`, `iterator_apply()`.

## Gotchas
- `iterator_to_array($it, preserve_keys: true)` (the default) overwrites values with duplicate keys, the last value wins; pass `false` to get every value.- `Generator::rewind()` executes the generator up to and including the first `yield`; a generator is single-pass, so return a fresh generator from each `getIterator()` call.
- `Countable::count()` is what `count()` calls; `iterator_count()` counts by iterating.

Verify: iterate the same aggregate twice and confirm both loops yield all elements.

## Checked
2026-11-03. Confirmed on the IteratorAggregate, Iterator, SPL iterators, iterator_to_array, iterator_count and Generator manual pages. Removed (not confirmed): the exact "already closed generator" exception text, 8.1 tentative return type remark, `RecursiveDirectoryIterator`/`SKIP_DOTS` example, ArrayObject modification claim.
Method: documentation only; no commands were run.
