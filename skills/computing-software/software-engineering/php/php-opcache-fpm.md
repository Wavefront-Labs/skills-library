---
id: computing-software.software-engineering.php.php-opcache-fpm
name: php-opcache-fpm
category: computing-software
field: software-engineering
product: php
tags: [php, php-runtime, opcache-fpm]
level: advanced
status: docs-checked
description: "Enable OPcache, size pools in PHP-FPM, and consider preloading and JIT carefully."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPcache and PHP-FPM tuning
- `opcache.enable=1`, `opcache.memory_consumption`, `opcache.max_accelerated_files`, `opcache.validate_timestamps=0` in production (reset cache on deploy via reload/`opcache_reset`).
- FPM `pm = dynamic|static|ondemand`; `pm.max_children` ~ (RAM for PHP) / (avg worker RSS); watch `pm.status_path` and slow log.
- JIT (8.0) helps CPU-bound code, rarely typical web apps; preloading needs care.
Verify: load test and check worker memory with `ps`/status page.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
