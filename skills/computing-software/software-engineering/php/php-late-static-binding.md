---
id: computing-software.software-engineering.php.php-late-static-binding
name: php-late-static-binding
category: computing-software
field: software-engineering
product: php
tags: [php, late-static-binding, oop]
level: advanced
status: docs-checked
description: "Use static:: vs self::, new static and static properties correctly for inheritable factories."
sources: ["https://www.php.net/manual/en/language.oop5.late-static-bindings.php", "https://www.php.net/manual/en/language.oop5.static.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Late static binding

`self::` and `__CLASS__` are resolved using the class in which the function is defined; `static::` is computed from runtime information, the class that was actually called.
```php
class Model {
    public static function create(): static { return new static(); }   // subclass instance
    public static function table(): string { return static::TABLE; }   // subclass constant
    public static function describe(): string { return self::class . '/' . static::class; }
}
class User extends Model { const TABLE = 'users'; }
User::create();            // a User
User::describe();          // "Model/User"
```
Late static binding resolution stops at a fully resolved static call with no fallback (`Model::create()` names the class). Calls with `parent::` or `self::` forward the calling information.

## Gotchas
- `new self` in a base class always builds the base class; use `new static` in factories.
- Static properties defined in both parent and child hold distinct values per class; those defined only in the parent share one common value. Use `self::` vs `static::` deliberately when reading or writing them. Redeclare a static property in each subclass to get per-class state.
- `static::CONST` requires every subclass (or the base) to define that constant.

Verify: print `static::class` from a subclass call and confirm it differs from `self::class`.

## Checked
2026-11-03. Confirmed on the Late Static Bindings and Static Keyword manual pages: `self::` vs `static::` resolution, forwarding and non-forwarding calls, static property inheritance. Removed (not on the pages): `static fn` closure remark, `new static` abstract/constructor failures, tooling advice, design opinion.
Method: documentation only; no commands were run.
