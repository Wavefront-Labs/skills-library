---
id: computing-software.software-engineering.php.php-psr12-style
name: php-psr12-style
category: computing-software
field: software-engineering
product: php
tags: [php, php-standards, psr12-style]
level: intro
status: docs-checked
description: "Apply the PSR-12 extended coding style: files, lines, headers, classes, methods and control structures."
sources: ["https://www.php-fig.org/psr/psr-12/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSR-12 coding style

PSR-12 extends and replaces PSR-2 and requires PSR-1 (StudlyCaps means PascalCase).

- Files: Unix LF only, end with one LF, omit the closing `?>` in PHP-only files.
- Lines: no hard limit, soft limit 120 characters, lines SHOULD be 80 or fewer; no trailing whitespace; one statement per line.
- Indent with 4 spaces, never tabs.
- Keywords and types lower case; short forms `bool`, `int`.
- File header order, each block separated by one blank line: `<?php`, file docblock, `declare(strict_types=1);`, namespace, class `use`, function `use`, const `use`, then code. Imports never start with a backslash.
- `new Foo();` always has parentheses.
- Class and method opening braces go on their own line; `extends` and `implements` stay on the class line.
- Visibility is required on properties and methods (and constants on PHP 7.1+). Do not use `var`, one property per statement, no underscore prefix to signal visibility.
- `abstract` and `final` come before visibility; `static` comes after.
- Arguments: no space before a comma, one after; with a split list put one argument per line, and `) {` on its own line. Return types are `): string`; nullable is `?string` with no space.
- Control structures: one space after the keyword, braces always present, opening brace on the same line, `elseif` rather than `else if`, `else`/`elseif` on the closing-brace line.

Verify: run your project's formatter or sniffer in CI as a check (tool choice and flags are not part of the standard).

## Checked

Date: 2026-11-08. Read PSR-12 sections 1 to 4 and the start of section 5 (control structures, `if`/`elseif`/`else`) in the php-fig markdown; the remaining control-structure sections (switch, loops, try, closures, operators) were not read, so nothing is claimed about them. Removed the PSR-1 rules (one class per file, constant naming) and the php-cs-fixer/phpcs commands, because those sources were not read.

Method: documentation only; no commands were run.
