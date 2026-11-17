---
id: computing-software.software-engineering.php.php-composer-audit
name: php-composer-audit
category: computing-software
field: software-engineering
product: php
tags: [php, composer-audit, supply-chain]
level: practitioner
status: docs-checked
description: "Scan PHP dependencies with composer audit, handle abandoned packages, configure ignores and gate CI."
sources: ["https://getcomposer.org/doc/03-cli.md", "https://getcomposer.org/doc/06-config.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composer audit and security advisories

`composer audit` checks installed packages against security advisories from the Packagist.org API (or repositories listed in `composer.json`). It also detects abandoned and malware-flagged packages and packages matched by other dependency policies. Exit code `0` means no issues; `1` means findings (or missing required packages).
```sh
composer audit
composer audit --locked              # audit composer.lock regardless of what is in vendor
composer audit --no-dev --direct     # skip require-dev; only directly required packages
composer audit --format=json         # table (default), plain, json, summary
composer audit --abandoned=fail      # ignore | report | fail
composer audit --ignore-severity=LEVEL # repeatable
composer install --audit             # also audit after installing
composer why-not vendor/pkg 3.0      # why can't I upgrade?
```
`update`, `require` and `remove` run audit steps after changing the lock file unless you pass `--no-audit`.

Exceptions and abandoned handling in `composer.json`. Current docs mark `config.audit` as deprecated in favour of `config.policy` (still supported for now, removal planned for a future major version): use `config.policy.advisories.ignore-id` for advisory IDs (CVE, GHSA, PKSA). If `config.policy.advisories` is set, every advisory-related `audit.*` key is ignored, so migrate those settings together. Legacy form:
```json
"config": { "audit": { "ignore": { "PKSA-xxxx-xxxx": "False positive: feature disabled" },
                        "abandoned": "report" } }
```
`audit.abandoned` takes `ignore`, `report` (reported but exit code unaffected) or `fail`; it defaults to `fail` since Composer 2.7. The `--abandoned` CLI option overrides it from Composer 2.8.

CI pattern: run `composer validate --strict`, `composer install`, then `composer audit --locked` on every PR and on a scheduled job, since new advisories appear against unchanged lock files.

## Gotchas
- `--locked` audits the lock file; otherwise the installed set is audited.
- Advisories cover Packagist packages, not PHP itself, extensions, system libraries or JavaScript assets; scan those separately.
- A fix may need a major upgrade; `composer bump` raises requirement lower bounds to installed versions (not recommended blindly on libraries).
- Record a reason (and review date) for every ignored advisory.

Verify: install an old version of a package with a known advisory in a scratch project and confirm `composer audit` exits 1 listing the advisory ID.

## Checked

Date: 2026-11-08. Read the `audit` section of the Composer CLI reference, the `install` and `update` option lists, and the `audit` configuration section including `ignore` and `abandoned` (current docs). Removed: the "Composer 2.4+" and "since 2.4 install warns" claims, the `--with-dependencies` example, the Satis/Private Packagist advisory claim, the `composer outdated --direct` suggestion, and the ignore-expiry wording. Config keys under `config.policy` beyond the names above were not read.

Method: documentation only; no commands were run.
