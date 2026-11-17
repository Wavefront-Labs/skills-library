---
id: computing-software.software-engineering.php.php-error-reporting-config
name: php-error-reporting-config
category: computing-software
field: software-engineering
product: php
tags: [php, php-errors, error-reporting-config]
level: practitioner
status: docs-checked
description: "Configure error_reporting, display_errors and log_errors for dev and production."
sources: ["https://www.php.net/manual/en/", "https://www.php-fig.org/psr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# error_reporting display_errors and logging
- Development: `error_reporting=E_ALL`, `display_errors=On`. Production: `display_errors=Off`, `log_errors=On`, `error_log=/path/to/log`; never show errors to users.
- Convert warnings to exceptions with `set_error_handler` + `ErrorException` and handle fatal shutdowns via `register_shutdown_function` and `error_get_last()`.
- `@` suppression hides useful errors; avoid.
Verify: `php -i | grep -E 'display_errors|error_reporting'`; trigger a warning in staging.

## Checked

Date: 2026-11-02. Confirmed against the PHP manual (php.net/manual/en) and, for Composer skills, getcomposer.org/doc: the functions, syntax, version gates and ini settings above. Removed or softened where the fetched pages did not state them (see the batch 843 findings).

Method: documentation only; no commands were run.
