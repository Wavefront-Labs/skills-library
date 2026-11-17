---
id: computing-software.software-engineering.php.php-namespaces-use
name: php-namespaces-use
category: computing-software
field: software-engineering
product: php
tags: [php, namespaces-use, namespaces]
level: intro
status: docs-checked
description: "Use PHP namespaces and use statements: name resolution rules, function imports, aliasing and the global fallback for functions and constants."
sources: ["https://www.php.net/manual/en/language.namespaces.rules.php", "https://www.php.net/manual/en/language.namespaces.basics.php", "https://www.php.net/manual/en/language.namespaces.fallback.php", "https://www.php.net/manual/en/language.namespaces.importing.php"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Namespaces and use statements

```php
<?php
declare(strict_types=1);
namespace App\Billing;

use App\Shared\Money;
use App\Shared\Contracts\Notifier as NotifierContract;     // alias
use function App\Shared\slugify;                             // function import
use InvalidArgumentException;                                // a global class needs an import or a leading backslash

final class Invoice {
    public function total(): Money {
        $len = strlen('abc');      // unqualified function: namespaced first, then falls back to global
        $c   = \count([]);         // fully qualified global function
        return new Money(10);
    }
}
```
Resolution rules from the manual: a fully qualified name starts with `\` and resolves to the name without the leading separator. An unqualified name is translated through the current import table for its symbol type (after `use A\B\C;`, `new C()` means `A\B\C`; after `use function A\B\foo;`, `foo()` means `A\B\foo`). With no import rule, a class-like name resolves in the current namespace, while an unqualified function or constant falls back to the global one if the namespaced one does not exist. A global class therefore needs a fully qualified name (`\Exception`) or a `use` import.

## Gotchas
- Forgetting to import a global class makes PHP look in the current namespace.
- Name resolution happens at compile time, so dynamic strings (`new $name`) need fully qualified names; `Foo::class` gives the resolved name.
- The fallback lets you provide a namespaced mock of a built-in function such as `time()`, if you call it unqualified.

Verify: run your static analyser or test suite for unknown-class errors.

## Checked
2026-11-03. Confirmed on the namespaces basics, name-resolution rules and fallback manual pages. Removed (not confirmed in fetched text): grouped `use` and `use const` examples, opcode-optimisation remark, PSR-1/4/12 conventions, Composer and case-sensitivity advice, bracketed-namespace advice.
Method: documentation only; no commands were run.
