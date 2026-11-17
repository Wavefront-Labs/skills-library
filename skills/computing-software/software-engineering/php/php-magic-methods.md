---
id: computing-software.software-engineering.php.php-magic-methods
name: php-magic-methods
category: computing-software
field: software-engineering
product: php
tags: [php, php-oop, magic-methods]
level: advanced
status: docs-checked
description: "Use static::, __get/__call/__invoke and Stringable correctly, and avoid overusing magic."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Late static binding magic methods and __toString
- `static::create()` resolves to the called class (late static binding); `self::` to the defining class.
- `__get`/`__set` run only for inaccessible/undefined properties; `__call`/`__callStatic`; `__invoke` makes objects callable; `__toString()` implicitly implements `Stringable` (8.0).
- Magic hurts static analysis: add `@property` or `@method` PHPDoc if needed.
Verify: PHPStan at level 6+ flags undefined property access.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
