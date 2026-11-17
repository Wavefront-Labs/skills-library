---
id: computing-software.software-engineering.php.php-rector-upgrades
name: php-rector-upgrades
category: computing-software
field: software-engineering
product: php
tags: [php, rector-upgrades, refactoring]
level: advanced
status: draft
description: "Automate PHP version and framework upgrades with Rector: rector.php sets, dry-run review, staged rules and CI checks."
sources: ["https://getrector.com/documentation", "https://github.com/rectorphp/rector"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Automated upgrades with Rector

Rector rewrites PHP using AST rules (language upgrades, type declarations, dead code, framework migrations).
```php
// rector.php
use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
return RectorConfig::configure()
    ->withPaths([__DIR__ . '/src', __DIR__ . '/tests'])
    ->withPhpSets(php83: true)            // newer config API; older versions use withSets([LevelSetList::UP_TO_PHP_83])
    ->withPreparedSets(deadCode: true, typeDeclarations: true)
    ->withSkip([Rector\Php80\Rector\Class_\ClassPropertyAssignToConstructorPromotionRector::class]);
```
```sh
vendor/bin/rector process --dry-run          # preview diffs
vendor/bin/rector process src/Billing        # apply to one directory
vendor/bin/rector process --clear-cache
```
Workflow: clean git tree, run one set at a time, review the diff, run tests and PHPStan, commit separately per set (one rule family per commit). Order: PHP version set, then type declarations, then dead code, then framework sets.

## Gotchas
- Rector can change behaviour (reorders, strictness, type coercion); never trust a bulk run without tests. Prioritise code with coverage.
- It needs your project to autoload (so it can resolve types); run `composer install` first and point `withAutoloadPaths` at vendor if needed.
- Config API changed between releases (`withPhpSets`/`withPreparedSets` are newer); use the docs for your version.
- Large codebases: use `--parallel` and a cache directory in CI.
- In CI, run `rector process --dry-run` and fail on diff to keep upgraded patterns from regressing.
- Pair with PHP-CS-Fixer to normalise formatting afterwards, not before.

Verify: after the run, tests and static analysis pass and `composer.json` `require.php` matches the sets applied.
