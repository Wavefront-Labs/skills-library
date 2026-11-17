---
id: computing-software.software-engineering.php.php-match-expression
name: php-match-expression
category: computing-software
field: software-engineering
product: php
tags: [php, php-functions, match-expression]
level: intro
status: docs-checked
description: "Use match instead of switch for strict, exhaustive value mapping."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# match expression
- `$r = match($code) { 200, 201 => 'ok', 404 => 'missing', default => throw new Exception() };` uses strict comparison, returns a value, has no fall-through.
- No matching arm and no default throws `UnhandledMatchError`.
- `match(true) { $x < 0 => ..., }` for conditions.
Verify: test an unmapped value triggers UnhandledMatchError.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
