---
id: computing-software.software-engineering.php.php-attributes
name: php-attributes
category: computing-software
field: software-engineering
product: php
tags: [php, php-oop, attributes]
level: advanced
status: docs-checked
description: "Declare and read native attributes (#[...]) via Reflection instead of docblock annotations."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attributes
- `#[Route('/x', methods: ['GET'])] class C {}` (PHP 8.0). Attribute classes are marked `#[Attribute]` with target flags.
- Read: `(new ReflectionClass($c))->getAttributes(Route::class)[0]->newInstance()`; attribute arguments must be constant expressions (8.1 allows `new` in initialisers).
- Unknown attribute classes are ignored until instantiated.
Verify: test reflection returns the attribute arguments you expect.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
