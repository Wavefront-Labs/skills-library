---
id: computing-software.software-engineering.php.php-closures-arrow-functions
name: php-closures-arrow-functions
category: computing-software
field: software-engineering
product: php
tags: [php, php-functions, closures-arrow-functions]
level: practitioner
status: docs-checked
description: "Choose between closures, arrow functions and first-class callable syntax, including scope capture."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures arrow functions and first-class callables
- `function() use ($x) { }` captures by value (use `&$x` for reference); `fn($y) => $x + $y` captures the parent scope by value automatically (7.4) and has one expression.
- First-class callable syntax `strlen(...)`, `$obj->method(...)`, `Foo::bar(...)` (8.1) creates a Closure.
- `static fn` / `static function` avoids binding `$this` and accidental leaks.
Verify: modify the captured variable after creating the closure and observe it unchanged.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
