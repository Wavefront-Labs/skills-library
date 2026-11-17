---
id: computing-software.software-engineering.php.php-php-cs-fixer
name: php-php-cs-fixer
category: computing-software
field: software-engineering
product: php
tags: [php, php-cs-fixer, code-style]
level: practitioner
status: draft
description: "Enforce PHP code style automatically with PHP-CS-Fixer or PHP_CodeSniffer: rulesets, dry-run diffs, caching and CI."
sources: ["https://cs.symfony.com/", "https://github.com/PHPCSStandards/PHP_CodeSniffer/wiki"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PHP-CS-Fixer and PHP_CodeSniffer

```php
// .php-cs-fixer.dist.php
$finder = PhpCsFixer\Finder::create()->in([__DIR__ . '/src', __DIR__ . '/tests'])->exclude('var');
return (new PhpCsFixer\Config())
    ->setRules(['@PER-CS' => true, '@PHP82Migration' => true, 'declare_strict_types' => true,
                'ordered_imports' => ['sort_algorithm' => 'alpha'], 'no_unused_imports' => true])
    ->setRiskyAllowed(true)
    ->setCacheFile(__DIR__ . '/var/.php-cs-fixer.cache')
    ->setFinder($finder);
```
```sh
vendor/bin/php-cs-fixer fix --dry-run --diff        # CI: exit non-zero when changes are needed
vendor/bin/php-cs-fixer fix                         # apply locally
vendor/bin/phpcs --standard=PSR12 src               # PHPCS reports; phpcbf fixes
```
Install per-project in `require-dev` (or in `tools/` with its own composer.json to avoid dependency conflicts).

## Gotchas
- Risky rules (`declare_strict_types`, `native_function_invocation`) can change behaviour; they need `setRiskyAllowed(true)` and tests.
- Pick one tool per concern: a formatter plus a static analyser (PHPStan) is common; two formatters fight each other.
- Run the formatter in a pre-commit hook on staged files only, plus the full dry-run in CI.
- Rule sets (`@Symfony`, `@PER-CS`) change between versions; pin the tool version and review diffs when upgrading.
- Large format-only commits obscure blame; add the commit to `.git-blame-ignore-revs`.

Verify: introduce a mis-ordered `use` statement, run with `--dry-run --diff` and expect a diff and exit code 8 (or non-zero); run again after `fix` and expect clean.
