---
id: computing-software.software-engineering.php.php-union-intersection-types
name: php-union-intersection-types
category: computing-software
field: software-engineering
product: php
tags: [php, union-intersection-types, types]
level: practitioner
status: docs-checked
description: "Use union, intersection, DNF and never/mixed types with the documented restrictions and the version each arrived in."
sources: ["https://www.php.net/manual/en/language.types.declarations.php", "https://www.php.net/manual/en/language.oop5.variance.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Union, intersection and never types

```php
function parse(int|string $id): User|null {}      // union
function save(Countable&Traversable $c): void {}  // intersection: all must hold (8.1)
function g((A&B)|null $x): void {}                // DNF types (8.2)
function fail(string $m): never { throw new RuntimeException($m); }   // return-only type (8.1)
function f(?int $x) {}                            // ?T is identical to T|null
```
Version history from the manual: intersection types and `never` 8.1.0; DNF types, and standalone `null` and `false` 8.2.0 (before 8.2.0 a union made only of these was not allowed, and intersection types could not be combined with unions); `mixed` 8.0.0.

## Gotchas
- `mixed` or `never` inside a union is an error. `iterable` cannot be combined with `array` or `Traversable` in the same union.
- Making a default of `null` the way to get a nullable argument is not recommended by the manual: use `?T` / `T|null`.
- Under `declare(strict_types=1)` arguments are not coerced; without it scalars may be coerced to a member of the union (the page has a worked example of the preference order).
- Return types are covariant and parameter types contravariant in subclasses; the variance page lists the rules and examples.

Verify: call a union-typed function with and without `strict_types` and inspect with `var_dump`.

## Checked
2026-11-03. Confirmed on the type declarations and variance manual pages. Removed (not confirmed in fetched text): `T|mixed` wording, `void` in unions, `callable` property restriction, intersection-of-scalars rule, uninitialized typed property behaviour, PHPStan/Psalm advice, the "1.5" coercion example.
Method: documentation only; no commands were run.
