---
id: computing-software.software-engineering.php.php-enums
name: php-enums
category: computing-software
field: software-engineering
product: php
tags: [php, php-oop, enums]
level: practitioner
status: docs-checked
description: "Model fixed value sets with enums, backed values, methods and interfaces."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enums backed and pure
- `enum Status: string { case Active = 'active'; public function label(): string { return ucfirst($this->value); } }` (PHP 8.1).
- `Status::from('x')` throws ValueError; `tryFrom` returns null; `Status::cases()` lists cases.
- Enums can implement interfaces and use traits (no state); constants allowed; they cannot be instantiated.
- Compare with `===`; use in `match`.
Verify: test from/tryFrom with invalid input.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
