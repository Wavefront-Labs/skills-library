---
id: computing-software.software-engineering.php.php-psr4-autoloading
name: php-psr4-autoloading
category: computing-software
field: software-engineering
product: php
tags: [php, php-composer, psr4-autoloading]
level: intro
status: docs-checked
description: "Configure PSR-4 autoload mappings in Composer and dump optimised autoloaders."
sources: ["https://www.php-fig.org/psr/psr-4/", "https://getcomposer.org/doc/01-basic-usage.md", "https://getcomposer.org/doc/03-cli.md#install--i"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PSR-4 autoloading

- Composer mapping: `"autoload": {"psr-4": {"Acme\\": "src/"}}`. Class `Acme\Foo` is then `src/Foo.php`; a sub-namespace maps to a subdirectory.
- PSR-4 rules: the fully qualified name needs a vendor (top-level) namespace and a class name; underscores have no special meaning; directory and file names must match the case of the namespace and class names (so case matters on case-sensitive filesystems); the file name ends in `.php`.
- After changing `autoload`, re-run `composer dump-autoload`, which regenerates `vendor/autoload.php`.
- Production: `composer install --optimize-autoloader` (`-o`) converts PSR-0/4 rules to a classmap; `--classmap-authoritative` (`-a`) loads from the classmap only and implies `-o`. Neither is the default. `--strict-psr-autoloader` fails with exit code 6 when mappings are wrong (needs `-o` or `-a`).
- Use `autoload-dev` for test classes; `--no-dev` skips those rules.
- An autoloader must not throw or raise errors (PSR-4).

Verify: `composer dump-autoload -o` and a smoke test that instantiates a class from each namespace.

## Checked

Date: 2026-11-08. Read in full: PSR-4 specification and the Composer basic-usage page (autoloading section). Read the Composer CLI reference for `install` (optimizer flags, `--strict-psr-autoloader`, `--no-dev`). Removed claims about classmap mode and the "PSR-4 warnings" output of `dump-autoload`, which the pages do not state, and the unread php.net manual source. `autoload-dev` is named in the install `--no-dev` text only, not documented in detail on the pages read.

Method: documentation only; no commands were run.
