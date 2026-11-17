---
id: computing-software.software-engineering.php.php-phpstan-psalm
name: php-phpstan-psalm
category: computing-software
field: software-engineering
product: php
tags: [php, php-testing-analysis, phpstan-psalm]
level: practitioner
status: draft
description: "Adopt PHPStan or Psalm with a baseline and raise strictness gradually."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PHPStan and Psalm static analysis levels
- `phpstan.neon` with `level: 6`..`9` (max), `paths: [src]`; `vendor/bin/phpstan analyse`; generate `--generate-baseline` to accept existing errors, then forbid new ones.
- Add PHPDoc generics (`@template T`, `list<int>`, `array{id:int}`) to describe shapes.
- Psalm equivalent: `psalm.xml`, `psalm --set-baseline=...`.
Verify: CI fails on any new error.
