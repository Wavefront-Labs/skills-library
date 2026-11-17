---
id: computing-software.software-engineering.php.php-composer-scripts
name: php-composer-scripts
category: computing-software
field: software-engineering
product: php
tags: [php, php-composer, composer-scripts]
level: advanced
status: docs-checked
description: "Use Composer scripts, plugins allow-list and platform config safely."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composer scripts and platform config
- `"scripts": {"test": "phpunit", "post-install-cmd": [...]}` run with `composer test`; `@php`, `@composer` aliases.
- From Composer 2.2.0 `config.allow-plugins` restricts which plugins may run code; review any plugin before allowing.
- `config.platform.php` simulates the production PHP version for resolution.
- Never run `composer install` with untrusted `scripts` in CI without review.
Verify: `composer diagnose`.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
