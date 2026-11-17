---
id: computing-software.software-engineering.php.php-first-class-callable
name: php-first-class-callable
category: computing-software
field: software-engineering
product: php
tags: [php, first-class-callable, closures]
level: practitioner
status: docs-checked
description: "Create closures with strlen(...), $obj->method(...) and Foo::bar(...) (PHP 8.1) instead of string callables or Closure::fromCallable."
sources: ["https://www.php.net/manual/en/functions.first_class_callable_syntax.php", "https://www.php.net/manual/en/class.closure.php", "https://www.php.net/manual/en/closure.fromcallable.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# First-class callable syntax (PHP 8.1+)

```php
$f = strlen(...);                       // Closure for a function
$g = $formatter->format(...);           // method of an object
$h = Money::fromCents(...);             // static method
array_map(trim(...), $lines);
usort($users, $this->compareByAge(...));

// Older forms
Closure::fromCallable([$obj, 'method']);
```
`CallableExpr(...)` has the same semantics as `Closure::fromCallable()`. Unlike callables written as strings and arrays, it is accessible to static analysis and uses the scope at the point where the callable is acquired.

## Gotchas
- Visibility is checked where the `(...)` is written: `return $this->privateMethod(...);` inside the class works (identical to `Closure::fromCallable([$this, 'privateMethod'])`) and the closure can be passed out, whereas the array form `[$foo, 'privateMethod']` called from outside fails with "Call to private method".
- `new Foo(...)` is not supported, because `new Foo()` is not considered a call.
- It cannot be combined with the nullsafe operator: that is a compile-time error.
- Syntax is PHP 8.1+; below that it is a parse error.

Verify: `var_dump(strlen(...) instanceof Closure)` prints `bool(true)`.

## Checked
2026-11-03. Confirmed on the first-class callable syntax, Closure and Closure::fromCallable manual pages. Removed (not on the pages): dynamic-name forms, `__call` routing, generator note, `bindTo` and reflection remarks, composer.json advice.
Method: documentation only; no commands were run.
