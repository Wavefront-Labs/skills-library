---
id: computing-software.software-engineering.php.php-composer-versions
name: php-composer-versions
category: computing-software
field: software-engineering
product: php
tags: [php, php-composer, composer-versions]
level: practitioner
status: docs-checked
description: "Declare dependencies with semver constraints and manage composer.lock correctly."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# composer.json versions and lock file
- Constraints: `^1.2` (>=1.2.0 <2.0.0), `~1.2.3` (>=1.2.3 <1.3.0), `1.*`, exact; `composer require vendor/pkg`, `composer update vendor/pkg`, `composer install` installs exactly from the lock.
- Commit `composer.lock` for applications; run `composer install --no-dev --optimize-autoloader` in production; declare `php` and `ext-*` requirements.
- `composer why`, `composer why-not` explain conflicts; `composer audit` checks advisories.
Verify: CI uses `composer validate --strict`.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
