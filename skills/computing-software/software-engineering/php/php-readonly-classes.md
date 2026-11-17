---
id: computing-software.software-engineering.php.php-readonly-classes
name: php-readonly-classes
category: computing-software
field: software-engineering
product: php
tags: [php, readonly-classes, immutability]
level: practitioner
status: docs-checked
description: "Model immutable value objects with readonly properties (8.1) and readonly classes (8.2), withers, cloning rules (8.3, 8.5) and shallow immutability."
sources: ["https://www.php.net/manual/en/language.oop5.properties.php#language.oop5.properties.readonly-properties", "https://www.php.net/manual/en/migration82.new-features.php", "https://www.php.net/manual/en/migration83.new-features.php", "https://www.php.net/manual/en/language.oop5.cloning.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Readonly properties and classes

```php
final readonly class Money {                        // readonly class: PHP 8.2
    public function __construct(public int $cents, public string $currency) {}
    public function add(Money $o): static {
        return new static($this->cents + $o->cents, $this->currency);   // "wither" returns a new instance
    }
}
class Order {
    public function __construct(public readonly array $lines) {}       // readonly property: PHP 8.1
}
$m = new Money(100, 'EUR');
$m->cents = 5;   // Error: Cannot modify readonly property
```
Property rules from the manual: `readonly` (PHP 8.1.0) can only be applied to typed properties (use `mixed` for untyped); a readonly property can be initialised once, only from the scope where it was declared, by direct assignment; it cannot have a default value, cannot be `static`, and cannot be `unset()` once initialised. Readonly classes arrived in PHP 8.2 ("Support for readonly on classes has been added").

## Gotchas
- Readonly is shallow: objects (or resources) held in a readonly property can still be modified internally. Arrays cannot be modified indirectly (`Cannot indirectly modify readonly property`).
- As of PHP 8.3.0 readonly properties can be reinitialised during cloning in `__clone()`; before that, `clone` plus `__clone()` cannot change them. As of PHP 8.4.0 acquiring a reference to a readonly property inside `__clone()` is no longer allowed.
- As of PHP 8.5.0, `clone($obj, ['prop' => $value])` (clone as a function with a `withProperties` array) can update readonly properties on the copy, suiting `with*()` methods.
- Before PHP 8.4.0 a readonly property is implicitly `private(set)`; from 8.4.0 it is `protected(set)`, so child classes may set it.
- A project on PHP 8.1 cannot use `readonly class`; match the syntax to the minimum PHP version you support.

Verify: attempt a write from outside the class and expect `Error`.

## Checked
2026-11-03. Confirmed on the properties (readonly section), PHP 8.2 and 8.3 new-features, and cloning manual pages. Removed (not confirmed): readonly-class-specific inheritance rules, dynamic-property ban, ORM hydration remark.
Method: documentation only; no commands were run.
