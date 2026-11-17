---
id: computing-software.software-engineering.php.php-php-ini-hardening
name: php-php-ini-hardening
category: computing-software
field: software-engineering
product: php
tags: [php, php-ini-hardening, security]
level: practitioner
status: docs-checked
description: "Harden php.ini for production: display_errors, expose_php, disable_functions, upload and session settings, and verify them."
sources: ["https://www.php.net/manual/en/ini.core.php", "https://www.php.net/manual/en/errorfunc.configuration.php", "https://www.php.net/manual/en/filesystem.configuration.php", "https://www.php.net/manual/en/session.configuration.php", "https://www.php.net/manual/en/install.fpm.configuration.php", "https://www.php.net/manual/en/configuration.changes.modes.php", "https://www.php.net/supported-versions.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# php.ini hardening

```ini
; production baseline (check each against your version's manual)
display_errors=Off
log_errors=On
error_log=/var/log/php/error.log
expose_php=Off
allow_url_fopen=Off            ; only if the app does not fetch URLs through fopen wrappers
allow_url_include=Off
open_basedir=/var/www/app:/tmp
disable_functions=exec,passthru,shell_exec,system,proc_open,popen
zend.assertions=-1
session.use_strict_mode=1
session.cookie_httponly=1
session.cookie_secure=1
session.cookie_samesite=Lax
session.use_only_cookies=1
```
Size limits (`upload_max_filesize`, `post_max_size`, `memory_limit`, `max_input_vars`) are listed in the manual's ini tables; set them to what the app needs, not to a copied number.

Per-pool overrides in PHP-FPM go in the pool config as `php_admin_value[name]` and `php_admin_flag[name]`. The FPM manual states settings defined this way cannot be overridden with `ini_set()`, while `php_value`/`php_flag` can be, and `disable_functions` set in a pool is appended to the php.ini value rather than replacing it.

## Facts from the manual
- `expose_php` is php.ini only; it exposes PHP and its version in the `X-Powered-By` header.
- `disable_functions` is INI_SYSTEM only (not httpd.conf). The manual warns it can be circumvented and is not a sufficient security measure for shared hosting. As of PHP 8.0.0 disabling a function removes its definition, so userland can redefine it. Only internal functions can be disabled.
- `allow_url_fopen` and `allow_url_include` are INI_SYSTEM; `allow_url_include` is deprecated as of PHP 7.4.0 and defaults to 0.
- `open_basedir` resolves symlinks, is a directory name not a prefix, and disables the realpath cache. A script can tighten it at runtime with `ini_set()`. It does not restrict Unix domain sockets.
- `zend.assertions=-1` generates no assertion code (production mode) and cannot be changed at runtime once the process starts that way.
- `session.sid_length` and `session.sid_bits_per_character`: changing from the defaults is deprecated as of PHP 8.4.0, so leave them alone on new versions.
- `session.use_strict_mode` defaults to 0; `session.use_only_cookies` defaults to 1.
- `display_errors`, `log_errors` and `error_log` are INI_ALL, so application code can change them with `ini_set()`; lock them with `php_admin_*` in FPM when that matters.

## Gotchas
- Disabling functions can break Composer, process runners and queue workers; use separate CLI settings.
- `session.*` settings are INI_ALL, so apps can override them; use `php_admin_*` to lock them.
- Turning `display_errors` off needs working logging (`log_errors`, `error_log`) with rotation set up outside PHP.
- Keep PHP on a supported branch (see the supported versions page) and apply security releases; hardening is not a patch substitute.

Verify: `curl -I` the app and confirm no `X-Powered-By` header; check the effective values in the SAPI that serves requests.

## Checked
2026-11-09. Confirmed on php.net manual pages ini.core, errorfunc.configuration, filesystem.configuration, session.configuration, install.fpm.configuration and configuration.changes.modes. Removed: the OWASP cheat sheet source, the sid_length/sid_bits settings, numeric size-limit examples, the lynis and `php -i | grep` verification, the claim that unknown directives are silently ignored, and the phpinfo-removal advice (not on the pages read).
Method: documentation only; no commands were run.
