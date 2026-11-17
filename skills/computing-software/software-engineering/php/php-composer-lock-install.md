---
id: computing-software.software-engineering.php.php-composer-lock-install
name: php-composer-lock-install
category: computing-software
field: software-engineering
product: php
tags: [php, composer-lock-install, composer]
level: practitioner
status: docs-checked
description: "Keep Composer installs reproducible: install vs update, lock file, platform config, optimized autoloader and production flags."
sources: ["https://getcomposer.org/doc/01-basic-usage.md", "https://getcomposer.org/doc/03-cli.md", "https://getcomposer.org/doc/06-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# composer.lock and reproducible installs

- `composer update` resolves `composer.json` constraints and writes the exact versions to `composer.lock`, then installs.
- `composer install` with a lock file present uses the exact locked versions (newer releases are ignored by design). Deploys and CI use `install`, not `update`. Without a lock file, `install` resolves and creates one.
- `composer update vendor/pkg` updates only that package; wildcards work (`"vendor/*"`). `-w` (`--with-dependencies`) also updates its dependencies except root requirements; `-W` (`--with-all-dependencies`) includes root requirements too. `--with vendor/pkg:2.0.1` adds a temporary constraint; `--lock` refreshes the lock file hash without changing versions.
- `composer require vendor/pkg:^2.1` edits `composer.json` and installs or updates; `--no-update` only edits the file.

Production install:
```sh
composer install --no-dev --optimize-autoloader
# stricter: --classmap-authoritative (-a), implies -o; or --apcu-autoloader
```
`--no-dev` skips `require-dev` packages and `autoload-dev` rules. `dist` downloads are the default.

Platform control, so resolution targets the runtime and not your laptop:
```json
"config": { "platform": { "php": "8.2.0" } }
```
Composer then assumes that PHP version and will not check the real one, so also run `composer check-platform-reqs` during deployment: it ignores `config.platform` and checks the real platform. `--ignore-platform-req=ext-foo` ignores one requirement; `{"ext-foo": false}` in `platform` hides a locally installed extension.

Validate with `composer validate --strict` (non-zero exit on warnings as well as errors).

## Gotchas
- Commit `composer.lock`. The Composer docs say libraries should commit it too.
- Composer warns on `install` when the lock file has not been updated since `composer.json` changes that affect resolution.
- Do not hand-merge a lock file; resolve `composer.json`, then run `composer update` for the affected packages (or `composer update --lock` to refresh only the hash).
- `--classmap-authoritative` loads classes from the classmap only.
- `--prefer-lowest` and `--prefer-stable` on `update` test minimum versions.

Verify: after a clean `composer install` in CI, `git diff --exit-code composer.lock` shows no change and `composer check-platform-reqs` passes.

## Checked

Date: 2026-11-08. Read in full: Composer basic usage. Read the CLI reference sections for `install`, `update` (options), `require`, `bump`, `check-platform-reqs` and `validate --strict`; and the config reference sections `platform` and `audit`. Removed: `composer diff`, `show -D`, `sort-packages` example, `--prefer-dist` and `--no-interaction` flags, the root and `--no-scripts`/`--no-plugins` advice, and the "content-hash" explanation (not stated on pages read). Corrected the claim that libraries may skip the lock file.

Method: documentation only; no commands were run.
