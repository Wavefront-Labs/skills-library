---
id: computing-software.software-engineering.php.php-datetime-immutable
name: php-datetime-immutable
category: computing-software
field: software-engineering
product: php
tags: [php, php-runtime, datetime-immutable]
level: practitioner
status: docs-checked
description: "Use DateTimeImmutable, DateTimeZone and DateInterval to avoid mutation and DST bugs."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Date and time with DateTimeImmutable
- Prefer `DateTimeImmutable` (methods return new objects); store UTC, convert for display: `new DateTimeImmutable('now', new DateTimeZone('UTC'))`, `->setTimezone(new DateTimeZone('Europe/Paris'))`.
- Format with `format('c')`; parse strictly with `DateTimeImmutable::createFromFormat` and check `getLastErrors()`.
- Check the `modify()` docs for end-of-month behaviour before relying on `+1 month`.
Verify: tests across DST transitions.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
