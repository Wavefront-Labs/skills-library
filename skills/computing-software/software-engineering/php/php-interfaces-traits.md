---
id: computing-software.software-engineering.php.php-interfaces-traits
name: php-interfaces-traits
category: computing-software
field: software-engineering
product: php
tags: [php, php-oop, interfaces-traits]
level: practitioner
status: docs-checked
description: "Pick interfaces, abstract classes or traits and resolve trait conflicts."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interfaces abstract classes and traits
- Interface: contract, multiple allowed. Abstract class: shared state/behaviour, single inheritance. Trait: horizontal code reuse; conflicts resolved with `insteadof` and `as`.
- Traits can declare abstract methods, static members and (8.2) constants; each using class gets its own static property copies.
- Prefer composition and injection over deep inheritance; mark classes `final` by default.
Verify: static analysis (PHPStan) reports unimplemented abstract members.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
