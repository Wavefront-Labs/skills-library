---
id: computing-software.cybersecurity-defensive.system-hardening.php-hardening
name: php-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [php-hardening, php-ini, php-fpm, disable-functions, open-basedir, web-server-hardening]
level: practitioner
status: docs-checked
description: "Harden PHP runtimes: php.ini settings for errors, sessions, uploads and remote includes, disable_functions and open_basedir limits, PHP-FPM pool isolation, and version support."
sources: ["https://www.php.net/manual/en/security.php", "https://www.php.net/manual/en/ini.list.php", "https://cheatsheetseries.owasp.org/cheatsheets/PHP_Configuration_Cheat_Sheet.html", "https://www.php.net/supported-versions.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PHP hardening

## php.ini (production)
```ini
expose_php = Off
display_errors = Off
display_startup_errors = Off
log_errors = On
error_log = /var/log/php/error.log
allow_url_fopen = Off            ; unless the app fetches URLs; use a HTTP client library instead
allow_url_include = Off          ; remote file inclusion (deprecated, default Off)
file_uploads = On                ; Off if the app never accepts uploads
upload_max_filesize = 10M
post_max_size = 12M
max_input_vars = 1000
max_execution_time = 30
memory_limit = 256M
session.use_strict_mode = 1
session.use_only_cookies = 1
session.cookie_httponly = 1
session.cookie_secure = 1
session.cookie_samesite = Lax
session.sid_length = 48          ; changing it is deprecated as of PHP 8.4
session.sid_bits_per_character = 6
session.save_path = /var/lib/php/sessions/<pool>
cgi.fix_pathinfo = 0             ; for nginx + FPM setups vulnerable to path info abuse
```

## disable_functions and open_basedir
- `disable_functions = exec,passthru,shell_exec,system,proc_open,popen,pcntl_exec,show_source` (check the app
  first; some frameworks need `proc_open` for queues or mail). Limits webshell impact but is bypassable via
  bugs; not a sandbox.
- `open_basedir = /var/www/app/:/tmp/php-app/` restricts file functions to listed directories. Also
  bypass-prone historically; defence in depth only.

## PHP-FPM pools
One pool per application with its own Unix user (`user = app1`), socket permissions (`listen.owner`,
`listen.mode = 0660`), session and temp directories; `security.limit_extensions`; `php_admin_value[...]` for settings apps must not override with `ini_set`.
`pm.max_children` sized to avoid resource exhaustion.

## Web server integration
- Never let uploaded files be executed: deny PHP execution in upload directories (nginx `location ~* ^/uploads/.*\.php$ { deny all; }`).
- Only pass existing files to FPM (`try_files $uri =404;` before `fastcgi_pass`).
- Block access to `.env`, `composer.json`, `vendor/`, `.git/`, backup files.

## Versions and extensions
Run a supported PHP version (each branch gets two years of active support plus two years of security-only fixes; check php.net supported
versions); remove unneeded extensions; keep Composer dependencies updated.

## Verify
`curl -I` shows no `X-Powered-By: PHP`; a forced error shows a generic page; `php -i | grep -E 'allow_url_include|display_errors|disable_functions'`
shows hardened values for the FPM SAPI (check `phpinfo()` via a temporary protected page, then remove it);
a `.php` file in uploads returns 403.

## Checked
2026-10-28. Confirmed against official pages: php.ini directives and defaults (expose_php, allow_url_include deprecated since 7.4, session.*, cgi.fix_pathinfo, disable_functions, open_basedir; PHP manual ini list), supported-versions policy (php.net), OWASP PHP Configuration Cheat Sheet.
Removed or rewritten: the security.limit_extensions explanation and composer audit (not in the fetched pages).
Method: documentation only; no commands were run.
