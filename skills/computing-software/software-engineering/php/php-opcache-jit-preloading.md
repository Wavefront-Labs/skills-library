---
id: computing-software.software-engineering.php.php-opcache-jit-preloading
name: php-opcache-jit-preloading
category: computing-software
field: software-engineering
product: php
tags: [php, opcache-jit-preloading, performance]
level: advanced
status: docs-checked
description: "Configure OPcache memory, timestamp validation, JIT (8.0+) and preloading (7.4+), and avoid stale-code pitfalls."
sources: ["https://www.php.net/manual/en/opcache.configuration.php", "https://www.php.net/manual/en/opcache.preloading.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OPcache JIT and preloading

```ini
; php.ini / conf.d (these are INI_SYSTEM settings unless noted)
opcache.enable=1
opcache.memory_consumption=256           ; MB of shared memory; default 128
opcache.interned_strings_buffer=16       ; MB; default 8; taken from the shared memory above
opcache.max_accelerated_files=20000      ; rounded up to the next prime in a fixed list; default 10000; range 200-1000000
opcache.validate_timestamps=0            ; default 1; INI_ALL
opcache.jit=tracing                      ; PHP 8.0+
opcache.jit_buffer_size=64M              ; 0 disables the JIT
opcache.preload=/app/preload.php         ; PHP 7.4+, not supported on Windows
opcache.preload_user=www-data
```

## Facts from the manual
- `opcache.validate_timestamps`: when on, scripts are re-checked every `opcache.revalidate_freq` seconds (default 2; 0 checks every request). When off you must reset OPcache with `opcache_reset()` or `opcache_invalidate()`, or restart the web server, for file changes to take effect.
- `opcache.enable_cli` defaults to 0, so CLI scripts do not use the cache unless you enable it.
- `opcache.save_comments=0` can break libraries that parse doc comments for annotations (Doctrine, PHPUnit are named).
- `opcache.file_update_protection` (default 2 seconds) stops caching of very recently modified files; set 0 only if every file update is atomic.
- `opcache.jit` accepts `disable` (cannot be enabled at runtime), `off`, `tracing`/`on` (recommended for most users), `function`, or a four-digit CRTO integer; tracing equals 1254 and function equals 1205. The default was `tracing` before PHP 8.4 and is `disable` from 8.4.
- `opcache.jit_buffer_size` default was 0 before PHP 8.4 and is 64M from 8.4. With JIT enabled the shared memory segment holds the JIT buffer too (memory_consumption plus jit_buffer_size).
- Preloading runs the `opcache.preload` script once at server start (PHP-FPM, mod_php); functions, classes, interfaces and traits (not constants) in loaded files are then available to all requests. It trades baseline memory for speed, needs a process restart to clear, and is only practical in production. It is mostly pointless for CLI scripts.
- Preloading as root is refused unless `opcache.preload_user=root` (from PHP 8.3 not needed under the CLI or phpdbg SAPI).
- In the preload script, `include`/`require` executes files and preloads nested includes, so parents must be loaded first; `opcache_compile_file()` does not execute code and accepts any order, which suits code that is otherwise autoloaded.

Whether JIT or preloading helps depends on the application (measure with realistic load before and after); the manual does not quantify gains.

## Gotchas
- With timestamp validation off, deploys need a reset or restart, or stale code runs.
- Preloaded code changes need a PHP process restart.
- A very large `interned_strings_buffer` reduces the bytecode cache size, since it comes out of `memory_consumption`.

Verify: confirm the settings with `phpinfo()` or `ini_get()`, and compare p95 latency under the same load test before and after.

## Checked

Date: 2026-11-08. Read in full: the PHP manual OPcache runtime configuration and Preloading pages. Removed: example preload loop and framework generators, the `Xdebug disables JIT` and shared-hosting claims, `opcache_get_status()` fields, the `1255` JIT syntax (the page gives 1254 and 1205), the FPM restart wording and the claim that a missing parent skips a class with warnings, none of which the pages state.

Method: documentation only; no commands were run.
