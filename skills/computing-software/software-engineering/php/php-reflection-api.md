---
id: computing-software.software-engineering.php.php-reflection-api
name: php-reflection-api
category: computing-software
field: software-engineering
product: php
tags: [php, reflection-api, metaprogramming]
level: advanced
status: docs-checked
description: "Inspect classes, constructor parameters, types and attributes with the PHP Reflection API for DI, validation and tooling."
sources: ["https://www.php.net/manual/en/book.reflection.php", "https://www.php.net/manual/en/class.reflectionclass.php", "https://www.php.net/manual/en/class.reflectionattribute.php", "https://www.php.net/manual/en/class.reflectionnamedtype.php", "https://www.php.net/manual/en/class.reflectionuniontype.php", "https://www.php.net/manual/en/class.reflectionparameter.php", "https://www.php.net/manual/en/class.reflectionenum.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reflection API

```php
$rc = new ReflectionClass(OrderService::class);
$rc->isFinal(); $rc->getInterfaceNames(); $rc->newInstanceArgs([/* ... */]);
foreach ($rc->getConstructor()?->getParameters() ?? [] as $p) {   // getConstructor(): ?ReflectionMethod
    $t = $p->getType();                       // ReflectionNamedType | ReflectionUnionType | ... | null
    echo $p->getName(), ' ', $t instanceof ReflectionNamedType ? $t->getName() : (string)$t,
         $p->isDefaultValueAvailable() ? ' = ' . var_export($p->getDefaultValue(), true) : '', "\n";
}
foreach ($rc->getMethods(ReflectionMethod::IS_PUBLIC) as $m) {}
$attr = $rc->getAttributes(Route::class)[0] ?? null;   // getAttributes(?string $name = null, int $flags = 0)
$route = $attr?->newInstance();                         // instantiates the attribute class
(new ReflectionEnum(Suit::class))->getCases();
```
Typical uses: autowiring a DI container from constructor types, routing from attributes, hydrators, test helpers.

## Gotchas
- `ReflectionNamedType::isBuiltin()` and `ReflectionType::allowsNull()` tell you whether a type is a builtin and nullable; a union type exposes `ReflectionUnionType::getTypes()`.
- `getAttributes()` takes a `$flags` argument: `ReflectionAttribute::IS_INSTANCEOF` also matches subclasses of the named attribute class. `ReflectionAttribute::newInstance()` is what instantiates the attribute.
- `ReflectionClass::newInstanceWithoutConstructor()` exists and skips the constructor: use it knowingly.
- `ReflectionProperty` and `ReflectionMethod` have `setAccessible()` for non-public members.
- Reading private state breaks encapsulation; fine in frameworks and tests, a smell in domain code.
- Do not reflect on user-supplied class names without an allowlist.

Verify: reflect on a class with a union-typed constructor argument and print each type via `getTypes()`.

## Checked
2026-11-03. Confirmed on the ReflectionClass, ReflectionAttribute, ReflectionNamedType, ReflectionUnionType, ReflectionType, ReflectionParameter, ReflectionMethod, ReflectionProperty and ReflectionEnum manual pages (method names and signatures). Removed: performance and caching advice, claim that setAccessible is unnecessary since PHP 8.1, attribute validation timing, alias advice.
Method: documentation only; no commands were run.
