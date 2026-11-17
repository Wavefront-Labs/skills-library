---
id: computing-software.software-engineering.php.php-arrayaccess-countable
name: php-arrayaccess-countable
category: computing-software
field: software-engineering
product: php
tags: [php, arrayaccess-countable, interfaces]
level: practitioner
status: docs-checked
description: "Implement ArrayAccess, Countable and Stringable for collection-like value objects, with the documented count() and array_key_exists behaviour."
sources: ["https://www.php.net/manual/en/class.arrayaccess.php", "https://www.php.net/manual/en/class.stringable.php", "https://www.php.net/manual/en/function.count.php", "https://www.php.net/manual/en/language.oop5.magic.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ArrayAccess, Countable and Stringable

```php
final class Bag implements ArrayAccess, Countable, Stringable {
    private array $items = [];
    public function offsetExists(mixed $o): bool { return isset($this->items[$o]); }
    public function offsetGet(mixed $o): mixed { return $this->items[$o] ?? throw new OutOfBoundsException("No key"); }
    public function offsetSet(mixed $o, mixed $v): void { $o === null ? $this->items[] = $v : $this->items[$o] = $v; }  // $bag[] = x passes null
    public function offsetUnset(mixed $o): void { unset($this->items[$o]); }
    public function count(): int { return count($this->items); }
    public function __toString(): string { return implode(',', $this->items); }
}
$b = new Bag; $b['x'] = 1; $b[] = 2; count($b);
```
Any class with a `__toString()` method implicitly implements `Stringable` as of PHP 8.0.0; the manual recommends declaring it explicitly. Its main use is a `string|Stringable` parameter type.

## Gotchas
- `array_key_exists()` on an `ArrayAccess` object does not call `offsetExists()` (stated on the ArrayAccess page); use `isset()` or `$obj[...]`.
- Since 8.0.0 `count()` throws `TypeError` for a value that is neither an array nor `Countable`.
- A `Stringable` object is not accepted by a `string` parameter under strict typing; accept `string|Stringable`.
- Prefer explicit methods (`get`, `set`) for domain objects; array syntax hides errors.

Verify: exercise `isset`, append (`[]`), unset and `count()` on the object against a native array.

## Checked
2026-11-03. Confirmed on the ArrayAccess, Stringable, count() and magic-methods manual pages: method signatures, `array_key_exists` note, `TypeError` from 8.0.0, implicit `Stringable`. Removed: claims about `empty()` / `??` call order, indirect-modification notice, `sizeof` alias, array-key coercion, unfetched JsonSerializable claim.
Method: documentation only; no commands were run.
