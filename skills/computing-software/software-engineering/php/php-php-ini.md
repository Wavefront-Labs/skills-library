---
id: computing-software.software-engineering.php.php-php-ini
name: php-php-ini
category: computing-software
field: software-engineering
product: php
tags: [php, php-runtime, php-ini]
level: practitioner
status: docs-checked
description: "Find and tune the right php.ini for CLI and FPM and understand precedence of settings."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# php.ini settings and CLI vs FPM
- Different ini files for CLI and FPM: `php --ini`, and `phpinfo()` for FPM.
- Key settings: `memory_limit`, `max_execution_time` (CLI default 0), `post_max_size`, `upload_max_filesize`, `expose_php=Off`.
- Override per directory with `.user.ini` (FPM/CGI) or `php_value` (mod_php); `ini_set` for settings changeable at runtime.
Verify: `php -r 'echo ini_get("memory_limit");'` and via a web request.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
